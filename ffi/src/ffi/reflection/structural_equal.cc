/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */
/*
 * \file src/ffi/reflection/structural_equal.cc
 *
 * \brief Structural equal implementation.
 */
#include <tvm/ffi/container/array.h>
#include <tvm/ffi/container/map.h>
#include <tvm/ffi/container/ndarray.h>
#include <tvm/ffi/container/shape.h>
#include <tvm/ffi/reflection/accessor.h>
#include <tvm/ffi/reflection/structural_equal.h>
#include <tvm/ffi/string.h>

#include <unordered_map>

namespace tvm {
namespace ffi {
namespace reflection {

/**
 * \brief Internal Handler class for structural equal comparison.
 */
class StructEqualHandler {
 public:
  StructEqualHandler() = default;

  bool CompareAny(ffi::Any lhs, ffi::Any rhs) {
    using ffi::details::AnyUnsafe;
    const TVMFFIAny* lhs_data = AnyUnsafe::TVMFFIAnyPtrFromAny(lhs);
    const TVMFFIAny* rhs_data = AnyUnsafe::TVMFFIAnyPtrFromAny(rhs);
    if (lhs_data->type_index != rhs_data->type_index) {
      return false;
    }
    if (lhs_data->type_index < TypeIndex::kTVMFFIStaticObjectBegin) {
      // this is POD data, we can just compare the value
      return lhs_data->v_int64 == rhs_data->v_int64;
    }
    switch (lhs_data->type_index) {
      case TypeIndex::kTVMFFIStr:
      case TypeIndex::kTVMFFIBytes: {
        // compare bytes
        const BytesObjBase* lhs_str =
            AnyUnsafe::CopyFromAnyViewAfterCheck<const BytesObjBase*>(lhs);
        const BytesObjBase* rhs_str =
            AnyUnsafe::CopyFromAnyViewAfterCheck<const BytesObjBase*>(rhs);
        return Bytes::memncmp(lhs_str->data, rhs_str->data, lhs_str->size, rhs_str->size) == 0;
      }
      case TypeIndex::kTVMFFIArray: {
        return CompareArray(AnyUnsafe::MoveFromAnyAfterCheck<Array<Any>>(std::move(lhs)),
                            AnyUnsafe::MoveFromAnyAfterCheck<Array<Any>>(std::move(rhs)));
      }
      case TypeIndex::kTVMFFIMap: {
        return CompareMap(AnyUnsafe::MoveFromAnyAfterCheck<Map<Any, Any>>(std::move(lhs)),
                          AnyUnsafe::MoveFromAnyAfterCheck<Map<Any, Any>>(std::move(rhs)));
      }
      case TypeIndex::kTVMFFIShape: {
        return CompareShape(AnyUnsafe::MoveFromAnyAfterCheck<Shape>(std::move(lhs)),
                            AnyUnsafe::MoveFromAnyAfterCheck<Shape>(std::move(rhs)));
      }
      case TypeIndex::kTVMFFINDArray: {
        return CompareNDArray(AnyUnsafe::MoveFromAnyAfterCheck<NDArray>(std::move(lhs)),
                              AnyUnsafe::MoveFromAnyAfterCheck<NDArray>(std::move(rhs)));
      }
      default: {
        return CompareObject(AnyUnsafe::MoveFromAnyAfterCheck<ObjectRef>(std::move(lhs)),
                             AnyUnsafe::MoveFromAnyAfterCheck<ObjectRef>(std::move(rhs)));
      }
    }
  }

  bool CompareObject(ObjectRef lhs, ObjectRef rhs) {
    // NOTE: invariant: lhs and rhs are already the same type
    const TVMFFITypeInfo* type_info = TVMFFIGetTypeInfo(lhs->type_index());
    if (type_info->extra_info == nullptr) {
      return lhs.same_as(rhs);
    }
    auto structural_eq_hash_kind = type_info->extra_info->structural_eq_hash_kind;

    if (structural_eq_hash_kind == kTVMFFISEqHashKindUnsupported ||
        structural_eq_hash_kind == kTVMFFISEqHashKindUniqueInstance) {
      // use pointer comparison
      return lhs.same_as(rhs);
    }
    if (structural_eq_hash_kind == kTVMFFISEqHashKindConstTreeNode) {
      // fast path: constant tree node, pointer equality indicate equality and avoid content
      // comparison if false, we should still run content comparison
      if (lhs.same_as(rhs)) return true;
    }
    // check recorded mapping for DAG and fre var
    if (structural_eq_hash_kind == kTVMFFISEqHashKindDAGNode ||
        structural_eq_hash_kind == kTVMFFISEqHashKindFreeVar) {
      // if there is pre-recorded mapping, need to cross check the pointer equality after mapping
      auto it = equal_map_lhs_.find(lhs);
      if (it != equal_map_lhs_.end()) {
        return it->second.same_as(rhs);
      }
      // if rhs is mapped but lhs is not, it means lhs is a free var, return false
      if (equal_map_rhs_.count(rhs)) {
        return false;
      }
    }

    bool success = true;
    if (structural_eq_hash_kind == kTVMFFISEqHashKindFreeVar) {
      // we are in a free var case that is not yet mapped.
      // in this case, either map_free_vars_ should be set to true, or map_free_vars_ should be set
      if (!lhs.same_as(rhs) && !map_free_vars_) {
        success = false;
      }
    } else {
      // We recursively compare the fields the object
      ForEachFieldInfoWithEarlyStop(type_info, [&](const TVMFFIFieldInfo* field_info) {
        // skip fields that are marked as structural eq hash ignore
        if (field_info->flags & kTVMFFIFieldFlagBitMaskSEqHashIgnore) return false;
        // get the field value from both side
        FieldGetter getter(field_info);
        Any lhs_value = getter(lhs);
        Any rhs_value = getter(rhs);
        // field is in def region, enable free var mapping
        if (field_info->flags & kTVMFFIFieldFlagBitMaskSEqHashDef) {
          bool allow_free_var = true;
          std::swap(allow_free_var, map_free_vars_);
          success = CompareAny(lhs_value, rhs_value);
          std::swap(allow_free_var, map_free_vars_);
        } else {
          success = CompareAny(lhs_value, rhs_value);
        }
        if (!success) {
          // record the first mismatching field if we sub-rountine compare failed
          if (mismatch_lhs_reverse_path_ != nullptr) {
            mismatch_lhs_reverse_path_->emplace_back(
                AccessStep::ObjectField(String(field_info->name)));
            mismatch_rhs_reverse_path_->emplace_back(
                AccessStep::ObjectField(String(field_info->name)));
          }
          // return true to indicate early stop
          return true;
        } else {
          // return false to continue checking other fields
          return false;
        }
      });
    }
    if (success) {
      // if we have a success mapping and in graph/var mode, record the equality mapping
      if (structural_eq_hash_kind == kTVMFFISEqHashKindDAGNode ||
          structural_eq_hash_kind == kTVMFFISEqHashKindFreeVar) {
        // record the equality
        equal_map_lhs_[lhs] = rhs;
        equal_map_rhs_[rhs] = lhs;
      }
      return true;
    } else {
      return false;
    }
  }

  bool CompareMap(Map<Any, Any> lhs, Map<Any, Any> rhs) {
    if (lhs.size() != rhs.size()) {
      // size mismatch, and there is no path tracing
      // return false since we don't need informative error message
      if (mismatch_lhs_reverse_path_ == nullptr) return false;
    }
    // compare key and value pair by pair
    for (auto kv : lhs) {
      Any rhs_key = this->MapLhsToRhs(kv.first);
      auto it = rhs.find(rhs_key);
      if (it == rhs.end()) {
        if (mismatch_lhs_reverse_path_ != nullptr) {
          mismatch_lhs_reverse_path_->emplace_back(AccessStep::MapKey(kv.first));
          mismatch_rhs_reverse_path_->emplace_back(AccessStep::MapKeyMissing(rhs_key));
        }
        return false;
      }
      // now recursively compare value
      if (!CompareAny(kv.second, (*it).second)) {
        if (mismatch_lhs_reverse_path_ != nullptr) {
          mismatch_lhs_reverse_path_->emplace_back(AccessStep::MapKey(kv.first));
          mismatch_rhs_reverse_path_->emplace_back(AccessStep::MapKey(rhs_key));
        }
        return false;
      }
    }
    // fast path, all contents equals to each other
    if (lhs.size() == rhs.size()) return true;
    // slow path, cross check every key from rhs in lhs to find the missing
    // key for better error reporting
    for (auto kv : rhs) {
      Any lhs_key = this->MapRhsToLhs(kv.first);
      auto it = lhs.find(lhs_key);
      if (it == lhs.end()) {
        if (mismatch_lhs_reverse_path_ != nullptr) {
          mismatch_lhs_reverse_path_->emplace_back(AccessStep::MapKeyMissing(lhs_key));
          mismatch_rhs_reverse_path_->emplace_back(AccessStep::MapKey(kv.first));
        }
        return false;
      }
    }
    return false;
  }

  bool CompareArray(ffi::Array<Any> lhs, ffi::Array<Any> rhs) {
    if (lhs.size() != rhs.size()) {
      // fast path, size mismatch, and there is no path tracing
      // return false since we don't need informative error message
      if (mismatch_lhs_reverse_path_ == nullptr) return false;
    }
    for (size_t i = 0; i < std::min(lhs.size(), rhs.size()); ++i) {
      if (!CompareAny(lhs[i], rhs[i])) {
        if (mismatch_lhs_reverse_path_ != nullptr) {
          mismatch_lhs_reverse_path_->emplace_back(AccessStep::ArrayIndex(i));
          mismatch_rhs_reverse_path_->emplace_back(AccessStep::ArrayIndex(i));
        }
        return false;
      }
    }
    if (lhs.size() == rhs.size()) return true;
    if (mismatch_lhs_reverse_path_ != nullptr) {
      if (lhs.size() > rhs.size()) {
        mismatch_lhs_reverse_path_->emplace_back(AccessStep::ArrayIndex(rhs.size()));
        mismatch_rhs_reverse_path_->emplace_back(AccessStep::ArrayIndexMissing(rhs.size()));
      } else {
        mismatch_lhs_reverse_path_->emplace_back(AccessStep::ArrayIndexMissing(lhs.size()));
        mismatch_rhs_reverse_path_->emplace_back(AccessStep::ArrayIndex(lhs.size()));
      }
    }
    return false;
  }

  bool CompareShape(Shape lhs, Shape rhs) {
    if (lhs.size() != rhs.size()) {
      return false;
    }
    for (size_t i = 0; i < lhs.size(); ++i) {
      if (lhs[i] != rhs[i]) {
        return false;
      }
    }
    return true;
  }

  bool CompareNDArray(NDArray lhs, NDArray rhs) {
    if (lhs.same_as(rhs)) return true;
    if (lhs->ndim != rhs->ndim) return false;
    for (int i = 0; i < lhs->ndim; ++i) {
      if (lhs->shape[i] != rhs->shape[i]) return false;
    }
    if (lhs->dtype != rhs->dtype) return false;
    if (!skip_ndarray_content_) {
      TVM_FFI_ICHECK_EQ(lhs->device.device_type, kDLCPU) << "can only compare CPU tensor";
      TVM_FFI_ICHECK_EQ(rhs->device.device_type, kDLCPU) << "can only compare CPU tensor";
      TVM_FFI_ICHECK(lhs.IsContiguous()) << "Can only compare contiguous tensor";
      TVM_FFI_ICHECK(rhs.IsContiguous()) << "Can only compare contiguous tensor";
      size_t data_size = GetDataSize(*(lhs.operator->()));
      return std::memcmp(lhs->data, rhs->data, data_size) == 0;
    } else {
      return true;
    }
  }

  Any MapLhsToRhs(Any lhs) const {
    if (lhs.type_index() < TypeIndex::kTVMFFIStaticObjectBegin) {
      return lhs;
    }
    ObjectRef lhs_obj = ffi::details::AnyUnsafe::MoveFromAnyAfterCheck<ObjectRef>(std::move(lhs));
    auto it = equal_map_lhs_.find(lhs_obj);
    if (it != equal_map_lhs_.end()) {
      return it->second;
    }
    return lhs_obj;
  }

  Any MapRhsToLhs(Any rhs) const {
    if (rhs.type_index() < TypeIndex::kTVMFFIStaticObjectBegin) {
      return rhs;
    }
    ObjectRef rhs_obj = ffi::details::AnyUnsafe::MoveFromAnyAfterCheck<ObjectRef>(std::move(rhs));
    auto it = equal_map_rhs_.find(rhs_obj);
    if (it != equal_map_rhs_.end()) {
      return it->second;
    }
    return rhs_obj;
  }
  // whether we map free variables that are not defined
  bool map_free_vars_{false};
  // whether we compare ndarray data
  bool skip_ndarray_content_{false};
  // the root lhs for result printing
  std::vector<AccessStep>* mismatch_lhs_reverse_path_ = nullptr;
  std::vector<AccessStep>* mismatch_rhs_reverse_path_ = nullptr;
  // map from lhs to rhs
  std::unordered_map<ObjectRef, ObjectRef, ObjectPtrHash, ObjectPtrEqual> equal_map_lhs_;
  // map from rhs to lhs
  std::unordered_map<ObjectRef, ObjectRef, ObjectPtrHash, ObjectPtrEqual> equal_map_rhs_;
};

bool StructuralEqual::Equal(const Any& lhs, const Any& rhs, bool map_free_vars,
                            bool skip_ndarray_content) {
  StructEqualHandler handler;
  handler.map_free_vars_ = map_free_vars;
  handler.skip_ndarray_content_ = skip_ndarray_content;
  return handler.CompareAny(lhs, rhs);
}

Optional<AccessPathPair> StructuralEqual::GetFirstMismatch(const Any& lhs, const Any& rhs,
                                                           bool map_free_vars,
                                                           bool skip_ndarray_content) {
  StructEqualHandler handler;
  handler.map_free_vars_ = map_free_vars;
  handler.skip_ndarray_content_ = skip_ndarray_content;
  std::vector<AccessStep> lhs_reverse_path;
  std::vector<AccessStep> rhs_reverse_path;
  handler.mismatch_lhs_reverse_path_ = &lhs_reverse_path;
  handler.mismatch_rhs_reverse_path_ = &rhs_reverse_path;
  if (handler.CompareAny(lhs, rhs)) {
    return std::nullopt;
  }
  AccessPath lhs_path(lhs_reverse_path.rbegin(), lhs_reverse_path.rend());
  AccessPath rhs_path(rhs_reverse_path.rbegin(), rhs_reverse_path.rend());
  return AccessPathPair(lhs_path, rhs_path);
}

TVM_FFI_STATIC_INIT_BLOCK({
  namespace refl = tvm::ffi::reflection;
  refl::GlobalDef().def("ffi.reflection.GetFirstStructuralMismatch",
                        StructuralEqual::GetFirstMismatch);
});

}  // namespace reflection
}  // namespace ffi
}  // namespace tvm
