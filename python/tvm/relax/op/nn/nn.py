# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
"""Relax Neural Network (NN) operators"""
from typing import List, Optional, Tuple, Union

from tvm import DataType, relax
from tvm.tir import FloatImm

from ...expr import Expr
from . import _ffi_api


def conv1d(
    data: Expr,
    weight: Expr,
    strides: Union[int, Tuple[int]] = 1,
    padding: Union[int, Tuple[int, ...]] = 0,
    dilation: Union[int, Tuple[int]] = 1,
    groups: int = 1,
    data_layout: str = "NCW",
    kernel_layout: str = "OIW",
    out_layout: Optional[str] = None,
    out_dtype: Optional[Union[str, DataType]] = None,
) -> Expr:
    r"""1D convolution.

    This operator takes the weight as the 1D convolution kernel
    and convolves it with data to produce an output.


    In the default case, where the data_layout is `NCW`
    and kernel_layout is `OIW`, conv1d takes in
    a data Tensor with shape `(batch_size, in_channels, width)`,
    and a weight Tensor with shape `(channels, in_channels, kernel_w)`,
    where `kernel_w` is the length of the `W` kernel dimension,
    to produce an output Tensor with the following rule:

    .. math::

        \mbox{out}[b, c, x] = \sum_{dx, k}
           \mbox{data}[b, k, \mbox{strides} * x + dx] *
           \mbox{weight}[c, k, dx]

    Padding and dilation are applied to data and weight respectively before the computation.
    This operator accepts data layout specification.
    Semantically, the operator will convert the layout to the canonical layout
    (`NCW` for data and `OIW` for weight), perform the computation,
    then convert to the out_layout.

    Parameters
    ----------
    data : relax.Expr
        The input data to the operator.

    weight : relax.Expr
        The weight expressions.

    strides : Union[int, Tuple[int]]
        The strides of convolution. It is required to have length 1.

    padding : Union[int, Tuple[int, ...]]
        The padding of convolution on both sides of inputs before convolution.
        It is required to have length either 1 or 2.

    dilation : Union[int, Tuple[int, int]]
        Specifies the dilation rate to be used for dilated convolution.
        It is required to have length 1.

    groups : int
        Number of groups to split the input into for grouped convolution.
        The number of input and output channels should be divisible by the number of groups.

    data_layout : str
        Layout of the input.

    kernel_layout : str
        Layout of the weight.

    out_layout : Optional[str]
        Layout of the output. If not specified, it is the same as data_layout

    out_dtype : Optional[Union[str, DataType]]
        Specifies the output data type for mixed precision conv1d.

    Returns
    -------
    result : relax.Expr
        The computed result.
    """
    if isinstance(strides, int):
        strides = (strides,)
    if isinstance(dilation, int):
        dilation = (dilation,)
    if isinstance(padding, int):
        padding = (padding, padding)

    return _ffi_api.conv1d(  # type: ignore
        data,
        weight,
        strides,
        padding,
        dilation,
        groups,
        data_layout,
        kernel_layout,
        out_layout,
        out_dtype,
    )


def conv2d(
    data: Expr,
    weight: Expr,
    strides: Union[int, Tuple[int, int]] = (1, 1),
    padding: Union[int, Tuple[int, ...]] = (0, 0),
    dilation: Union[int, Tuple[int, int]] = (1, 1),
    groups: int = 1,
    data_layout: str = "NCHW",
    kernel_layout: str = "OIHW",
    out_layout: Optional[str] = None,
    out_dtype: Optional[Union[str, DataType]] = None,
) -> Expr:
    r"""2D convolution.

    This operator takes the weight as the convolution kernel
    and convolves it with data to produce an output.


    In the default case, where the data_layout is `NCHW`
    and kernel_layout is `OIHW`, conv2d takes in
    a data Tensor with shape `(batch_size, in_channels, height, width)`,
    and a weight Tensor with shape `(channels, in_channels, kernel_h, kernel_w)`,
    where `kernel_h` and `kernel_w` is the lengths of the `H` and `W` kernel dimensions,
    to produce an output Tensor with the following rule:

    .. math::

        \mbox{out}[b, c, y, x] = \sum_{dy, dx, k}
           \mbox{data}[b, k, \mbox{strides}[0] * y  + dy, \mbox{strides}[1] * x + dx] *
           \mbox{weight}[c, k, dy, dx]

    Padding and dilation are applied to data and weight respectively before the computation.
    This operator accepts data layout specification.
    Semantically, the operator will convert the layout to the canonical layout
    (`NCHW` for data and `OIHW` for weight), perform the computation,
    then convert to the out_layout.

    Parameters
    ----------
    data : relax.Expr
        The input data to the operator.

    weight : relax.Expr
        The weight expressions.

    strides : Union[int, Tuple[int, int]]
        The strides of convolution. It is required to have length either 1 or 2.

    padding : Union[int, Tuple[int, ...]]
        The padding of convolution on both sides of inputs before convolution.
        It is required to have length either 1, 2 or 4.

    dilation : Union[int, Tuple[int, int]]
        Specifies the dilation rate to be used for dilated convolution.
        It is required to have length either 1 or 2.

    groups : int
        Number of groups to split the input into for grouped convolution.
        The number of input and output channels should be divisible by the number of groups.

    data_layout : str
        Layout of the input.

    kernel_layout : str
        Layout of the weight.

    out_layout : Optional[str]
        Layout of the output. If not specified, it is the same as data_layout

    out_dtype : Optional[Union[str, DataType]]
        Specifies the output data type for mixed precision conv2d.

    Returns
    -------
    result : relax.Expr
        The computed result.
    """
    if isinstance(strides, int):
        strides = (strides, strides)
    if isinstance(dilation, int):
        dilation = (dilation, dilation)
    if isinstance(padding, int):
        padding = (padding, padding, padding, padding)

    return _ffi_api.conv2d(  # type: ignore
        data,
        weight,
        strides,
        padding,
        dilation,
        groups,
        data_layout,
        kernel_layout,
        out_layout,
        out_dtype,
    )


def conv3d(
    data: Expr,
    weight: Expr,
    strides: Union[int, Tuple[int, int]] = (1, 1, 1),
    padding: Union[int, Tuple[int, ...]] = (0, 0, 0),
    dilation: Union[int, Tuple[int, int]] = (1, 1, 1),
    groups: int = 1,
    data_layout: str = "NCDHW",
    kernel_layout: str = "OIDHW",
    out_layout: Optional[str] = None,
    out_dtype: Optional[Union[str, DataType]] = None,
) -> Expr:
    r"""3D convolution.

    This operator takes the weight as the convolution kernel
    and convolves it with data to produce an output.


    In the default case, where the data_layout is `NCDHW`
    and kernel_layout is `OIDHW`, conv3d takes in
    a data Tensor with shape `(batch_size, in_channels, depth, height, width)`,
    and a weight Tensor with shape `(channels, in_channels, kernel_d, kernel_h, kernel_w)`,
    where `kernel_d`, `kernel_h`, and `kernel_w` are the lengths of the `D`, `H`,
    and `W` kernel dimensions, to produce an output Tensor with the following rule:

    .. math::

        \mbox{out}[b, c, z, y, x] = \sum_{dz, dy, dx, k}
           \mbox{data}[b, k, \mbox{strides}[0] * z + dz,
           \mbox{strides}[1] * y  + dy,
           \mbox{strides}[2] * x + dx] *
           \mbox{weight}[c, k, dz, dy, dx]

    Padding and dilation are applied to data and weight respectively before the computation.
    This operator accepts data layout specification.
    Semantically, the operator will convert the layout to the canonical layout
    (`NCDHW` for data and `OIDHW` for weight), perform the computation,
    then convert to the out_layout.

    Parameters
    ----------
    data : relax.Expr
        The input data to the operator.

    weight : relax.Expr
        The weight expressions.

    strides : Union[int, Tuple[int, int, int]]
        The strides of convolution. It is required to have length either 1 or 3.

    padding : Union[int, Tuple[int, ...]]
        The padding of convolution on both sides of inputs before convolution.
        It is required to have length either 1, 3 or 6.

    dilation : Union[int, Tuple[int, int, int]]
        Specifies the dilation rate to be used for dilated convolution.
        It is required to have length either 1 or 3.

    groups : int
        Number of groups to split the input into for grouped convolution.
        The number of input and output channels should be divisible by the number of groups.

    data_layout : str
        Layout of the input.

    kernel_layout : str
        Layout of the weight.

    out_layout : Optional[str]
        Layout of the output. If not specified, it is the same as data_layout

    out_dtype : Optional[Union[str, DataType]]
        Specifies the output data type for mixed precision conv2d.

    Returns
    -------
    result : relax.Expr
        The computed result.
    """
    if isinstance(strides, int):
        strides = (strides, strides, strides)
    if isinstance(dilation, int):
        dilation = (dilation, dilation, dilation)
    if isinstance(padding, int):
        padding = (padding, padding, padding, padding, padding, padding)

    return _ffi_api.conv3d(  # type: ignore
        data,
        weight,
        strides,
        padding,
        dilation,
        groups,
        data_layout,
        kernel_layout,
        out_layout,
        out_dtype,
    )


def conv1d_transpose(
    data: Expr,
    weight: Expr,
    strides: Union[int, Tuple[int]] = 1,
    padding: Union[int, Tuple[int, ...]] = 0,
    output_padding: Union[int, Tuple[int]] = 0,
    dilation: Union[int, Tuple[int]] = 1,
    groups: int = 1,
    data_layout: str = "NCW",
    kernel_layout: str = "IOW",
    out_layout: Optional[str] = None,
    out_dtype: Optional[Union[str, DataType]] = None,
) -> Expr:
    r"""1D transposed convolution operator.

    This operator can be seen as the gradient operator of conv1d.

    The output shape can be explained in the simple case when `data_layout == "NCW"` and
    `kernel_layout == "IOW"`. Suppose `data` has shape `(N, in_channel, in_w)`, `weight` has
    shape `(in_channel, out_channel, weight_w)`, we need to assure that `in_channel % groups == 0`.
    The shape of the output will be `(N, out_channel * groups, out_w)`, where

    - `out_w = ((in_w - 1) * strides[0] + weight_w - 2 * padding[0] + output_padding[0])`

    Parameters
    ----------
    data : relax.Expr
        The input data to the operator.

    weight : relax.Expr
        The weight expressions.

    strides : Union[int, Tuple[int]]
        The strides of convolution. It is required to have length 1.

    padding : Union[int, Tuple[int, ...]]
        The padding of convolution on both sides of inputs before convolution.
        It is required to have length either 1 or 2.

    output_padding : Union[int, Tuple[int, ...]], optional
        Used to disambiguate the output shape.

    dilation : Union[int, Tuple[int]]
        Specifies the dilation rate to be used for dilated convolution.
        It is required to have length either 1.

    groups : int
        Number of groups to split the input into for grouped convolution.
        The number of input and output channels should be divisible by the number of groups.

    data_layout : str
        Layout of the input.

    kernel_layout : str
        Layout of the weight.

    out_layout : Optional[str]
        Layout of the output. If not specified, it is the same as data_layout

    out_dtype : Optional[Union[str, DataType]]
        Specifies the output data type for mixed precision conv2d.

    Returns
    -------
    result : relax.Expr
        The computed result.
    """
    if isinstance(strides, int):
        strides = (strides,)
    if isinstance(dilation, int):
        dilation = (dilation,)
    if isinstance(padding, int):
        padding = (padding, padding)
    if isinstance(output_padding, int):
        output_padding = (output_padding,)

    return _ffi_api.conv1d_transpose(  # type: ignore
        data,
        weight,
        strides,
        padding,
        output_padding,
        dilation,
        groups,
        data_layout,
        kernel_layout,
        out_layout,
        out_dtype,
    )


def conv2d_transpose(
    data: Expr,
    weight: Expr,
    strides: Union[int, Tuple[int, int]] = (1, 1),
    padding: Union[int, Tuple[int, ...]] = (0, 0),
    output_padding: Union[int, Tuple[int, int]] = (0, 0),
    dilation: Union[int, Tuple[int, int]] = (1, 1),
    groups: int = 1,
    data_layout: str = "NCHW",
    kernel_layout: str = "IOHW",
    out_layout: Optional[str] = None,
    out_dtype: Optional[Union[str, DataType]] = None,
) -> Expr:
    r"""Two dimensional transposed convolution operator.

    This operator is intended to be the gradient operator of conv2d. That means, if

    `out = conv2d(data, weight, strides, padding, dilation)`,

    The gradient w.r.t. data can be calculated as follows:

    `data_grad = conv2d_transpose(out_grad, weight, strides, padding, output_padding, dilation)`,

    where `output_padding` is a parameter used to determine the output shape.

    The output shape can be explained in the simple case when `data_layout == "NCHW"` and
    `kernel_layout == "IOHW"`. Suppose `data` has shape `(N, in_channel, in_h, in_w)`, `weight` has
    shape `(in_channel, out_channel, weight_h, weight_w)`, we need to assure that
    `in_channel % groups == 0`. The shape of the output will be
    `(N, out_channel * groups, out_h, out_w)`, where

    - `out_h = ((in_h - 1) * strides[0] + weight_h - 2 * padding[0] + output_padding[0])`
    - `out_w = ((in_w - 1) * strides[1] + weight_w - 2 * padding[1] + output_padding[1])`

    Parameters
    ----------
    data : relax.Expr
        The input data to the operator.

    weight : relax.Expr
        The weight expressions.

    strides : Union[int, Tuple[int, int]]
        The strides of convolution. It is required to have length either 1 or 2.

    padding : Union[int, Tuple[int, ...]]
        The padding of convolution on both sides of inputs before convolution.
        It is required to have length either 1, 2 or 4.

    output_padding : Union[int, Tuple[int, ...]], optional
        Used to disambiguate the output shape.

    dilation : Union[int, Tuple[int, int]]
        Specifies the dilation rate to be used for dilated convolution.
        It is required to have length either 1 or 2.

    groups : int
        Number of groups to split the input into for grouped convolution.
        The number of input and output channels should be divisible by the number of groups.

    data_layout : str
        Layout of the input.

    kernel_layout : str
        Layout of the weight.

    out_layout : Optional[str]
        Layout of the output. If not specified, it is the same as data_layout

    out_dtype : Optional[Union[str, DataType]]
        Specifies the output data type for mixed precision conv2d.

    Returns
    -------
    result : relax.Expr
        The computed result.
    """
    # TODO: symbolic shape is not fully supported now
    if isinstance(strides, int):
        strides = (strides, strides)
    if isinstance(dilation, int):
        dilation = (dilation, dilation)
    if isinstance(padding, int):
        padding = (padding, padding, padding, padding)
    if isinstance(output_padding, int):
        output_padding = (output_padding, output_padding)

    return _ffi_api.conv2d_transpose(  # type: ignore
        data,
        weight,
        strides,
        padding,
        output_padding,
        dilation,
        groups,
        data_layout,
        kernel_layout,
        out_layout,
        out_dtype,
    )


def pad(
    data: Expr,
    pad_width: Union[List[int], Tuple[int, ...]],
    pad_mode: Optional[str] = "constant",
    pad_value: Optional[float] = 0.0,
):
    r"""Padding

    This operator takes in a tensor and pads each axis by the specified
    widths using the specified value.

    Parameters
    ----------
    data: relax.Expr
        The input data to the operator
    pad_width: Union[List[int], Tuple[int, ...]], required
        Number of values padded to the edges of each axis, in the format
        of ((before_1, after_1), ..., (before_N, after_N))
    pad_mode: Optional[str]
        'constant', 'reflect', 'replicate', 'circular'
        'constant' pads with constant value pad_value
        'reflect' pads by mirroring values excluding the edge
        'replicate' pads by repeating the edge values.
        'circular' pads by looping values from the other side
        Default is 'constant'
    pad_value: Optional[Union[float, Expr]]
        The value used for padding. Default is 0.

    Returns
    -------
    result : relax.Expr
        The computed result.
    """
    return _ffi_api.pad(data, pad_width, pad_mode, pad_value)


def pixel_shuffle(data: Expr, upscale_factor: int):
    r"""
    Pixel Shuffle Operator

    This operator performs the pixel shuffle operation on the input tensor,
    which is often used for efficient sub-pixel convolution in image
    super-resolution tasks. It rearranges elements in a tensor of shape
    (N, C × r^2, H, W) to a tensor of shape (N, C, H × r, W × r), where `r`
    is the upscale factor.

    Parameters
    ----------
    data : relax.Expr
        The input tensor to the pixel shuffle operator. It must have 4 dimensions
        with the format (N, C * r^2, H, W), where `r` is the upscale factor.

    upscale_factor : int
        The upscaling factor `r`. It determines how much to increase the spatial
        resolution (height and width) of the input tensor.

    Returns
    -------
    result : relax.Expr
        The transformed tensor with shape (N, C, H * r, W * r).

    Example
    -------
    If the input tensor has shape (1, 8, 10, 15) and `upscale_factor` is 2,
    the resulting tensor will have shape (1, 2, 20, 30).
    """
    return _ffi_api.pixel_shuffle(data, upscale_factor)


def max_pool1d(
    data: Expr,
    pool_size: Union[int, Tuple[int, int]] = (1,),
    strides: Union[int, Tuple[int, int]] = (1,),
    padding: Union[int, Tuple[int, ...]] = (0, 0),
    dilation: Union[int, Tuple[int, int]] = (1,),
    ceil_mode: bool = False,
    count_include_pad: bool = False,
    layout: str = "NCW",
    out_layout: Optional[str] = None,
) -> Expr:
    r"""1D maximum pooling operator.

    This operator takes data as input and does 1D max value calculation
    with in pool_size sized window by striding defined by stride.

    IIn the default case, where the data_layout is `NCW`
    a data Tensor with shape `(batch_size, channels, width)`,
    to produce an output Tensor.

    The ceil_mode is used to take ceil or floor while computing out shape.
    count_include_pad indicates including or excluding padded input values in computation.
    This operator accepts data layout specification.

    Parameters
    ----------
    data : relax.Expr
        The input data to the operator.

    pool_size : Union[int, Tuple[int, int]]
        The size of window for pooling. It is required to have length either 1.

    strides : Union[int, Tuple[int, int]]
        The strides of pooling. It is required to have length either 1.

    padding : Union[int, Tuple[int, ...]]
        The padding for pooling. It is required to have length either 1 or 2.

    dilation : Union[int, Tuple[int, int]]
        The dilation of pooling. It is required to have length either 1.

    ceil_mode : bool
        A boolean indicating if use ceil or floor to compute the output shape.
        By using ceil, every element in the input tensor will be covered by a sliding window.

    count_include_pad : bool, optional
        To include padding to compute the average.

    layout : str
        Layout of the input.

    out_layout : Optional[str]
        Layout of the output. If not specified, it is the same as data_layout

    Returns
    -------
    result : Expr
        The computed result.
    """
    if isinstance(pool_size, int):
        pool_size = (pool_size,)
    if isinstance(strides, int):
        strides = (strides,)
    if isinstance(dilation, int):
        dilation = (dilation,)
    if isinstance(padding, int):
        padding = (padding, padding)

    return _ffi_api.max_pool1d(  # type: ignore
        data,
        pool_size,
        strides,
        padding,
        dilation,
        ceil_mode,
        count_include_pad,
        layout,
        out_layout,
    )


def max_pool2d(
    data: Expr,
    pool_size: Union[int, Tuple[int, int]] = (1, 1),
    strides: Union[int, Tuple[int, int]] = (1, 1),
    padding: Union[int, Tuple[int, ...]] = (0, 0),
    dilation: Union[int, Tuple[int, int]] = (1, 1),
    ceil_mode: bool = False,
    count_include_pad: bool = False,
    layout: str = "NCHW",
    out_layout: Optional[str] = None,
) -> Expr:
    r"""2D maximum pooling operator.

    This operator takes data as input and does 2D max value calculation
    with in pool_size sized window by striding defined by stride.

    In the default case, where the data_layout is `NCHW`
    a data Tensor with shape `(batch_size, in_channels, height, width)`,
    to produce an output Tensor with the following rule:

    with data of shape (b, c, h, w) and pool_size (kh, kw)

    .. math::

        \mbox{out}(b, c, y, x)  = \max_{m=0, \ldots, kh-1} \max_{n=0, \ldots, kw-1}
             \mbox{data}(b, c, \mbox{stride}[0] * y + m, \mbox{stride}[1] * x + n)

    Padding is applied to data before the computation.
    ceil_mode is used to take ceil or floor while computing out shape.
    This operator accepts data layout specification.

    Parameters
    ----------
    data : relax.Expr
        The input data to the operator.

    pool_size : Union[int, Tuple[int, int]]
        The size of window for pooling. It is required to have length either 1 or 2.

    strides : Union[int, Tuple[int, int]]
        The strides of pooling. It is required to have length either 1 or 2.

    padding : Union[int, Tuple[int, ...]]
        The padding for pooling. It is required to have length either 1, 2 or 4.

    dilation : Union[int, Tuple[int, int]]
        The dilation of pooling. It is required to have length either 1 or 2.

    ceil_mode : bool
        A boolean indicating if use ceil or floor to compute the output shape.
        By using ceil, every element in the input tensor will be covered by a sliding window.

    count_include_pad : bool, optional
        To include padding to compute the average.

    layout : str
        Layout of the input.

    out_layout : Optional[str]
        Layout of the output. If not specified, it is the same as data_layout

    Returns
    -------
    result : Expr
        The computed result.
    """
    if isinstance(pool_size, int):
        pool_size = (pool_size, pool_size)
    if isinstance(strides, int):
        strides = (strides, strides)
    if isinstance(dilation, int):
        dilation = (dilation, dilation)
    if isinstance(padding, int):
        padding = (padding, padding, padding, padding)

    return _ffi_api.max_pool2d(  # type: ignore
        data,
        pool_size,
        strides,
        padding,
        dilation,
        ceil_mode,
        count_include_pad,
        layout,
        out_layout,
    )


def max_pool3d(
    data: Expr,
    pool_size: Union[int, Tuple[int, int]] = (1, 1, 1),
    strides: Union[int, Tuple[int, int]] = (1, 1, 1),
    padding: Union[int, Tuple[int, ...]] = (0, 0, 0),
    dilation: Union[int, Tuple[int, int]] = (1, 1, 1),
    ceil_mode: bool = False,
    count_include_pad: bool = False,
    layout: str = "NCDHW",
    out_layout: Optional[str] = None,
) -> Expr:
    r"""3D maximum pooling operator.

    This operator takes data as input and does 3D max value calculation
    with in pool_size sized window by striding defined by stride.


    In the default case, where the data_layout is `NCDHW`
    a data Tensor with shape `(batch_size, channels, depth, height, width)`,
    to produce an output Tensor.

    The ceil_mode is used to take ceil or floor while computing out shape.
    count_include_pad indicates including or excluding padded input values in computation.
    This operator accepts data layout specification.

    Parameters
    ----------
    data : relax.Expr
        The input data to the operator.

    pool_size : Union[int, Tuple[int, int]]
        The size of window for pooling. It is required to have length either 1 or 3.

    strides : Union[int, Tuple[int, int]]
        The strides of pooling. It is required to have length either 1 or 3.

    padding : Union[int, Tuple[int, ...]]
        The padding for pooling. It is required to have length either 1, 3 or 6.

    dilation : Union[int, Tuple[int, int]]
        The dilation of pooling. It is required to have length either 1 or 3.

    ceil_mode : bool
        A boolean indicating if use ceil or floor to compute the output shape.
        By using ceil, every element in the input tensor will be covered by a sliding window.

    count_include_pad : bool, optional
        To include padding to compute the average.

    layout : str
        Layout of the input.

    out_layout : Optional[str]
        Layout of the output. If not specified, it is the same as data_layout

    Returns
    -------
    result : Expr
        The computed result.
    """
    if isinstance(pool_size, int):
        pool_size = (pool_size, pool_size, pool_size)
    if isinstance(strides, int):
        strides = (strides, strides, strides)
    if isinstance(dilation, int):
        dilation = (dilation, dilation, dilation)
    if isinstance(padding, int):
        padding = (padding, padding, padding, padding, padding, padding)

    return _ffi_api.max_pool3d(  # type: ignore
        data,
        pool_size,
        strides,
        padding,
        dilation,
        ceil_mode,
        count_include_pad,
        layout,
        out_layout,
    )


def avg_pool1d(
    data: Expr,
    pool_size: Union[int, Tuple[int, int]] = (1,),
    strides: Union[int, Tuple[int, int]] = (1,),
    padding: Union[int, Tuple[int, ...]] = (0, 0),
    dilation: Union[int, Tuple[int, int]] = (1,),
    ceil_mode: bool = False,
    count_include_pad: bool = True,
    layout: str = "NCW",
    out_layout: Optional[str] = None,
) -> Expr:
    r"""1D average pooling operator.

    This operator takes data as input and does 1D average value calculation
    with in pool_size sized window by striding defined by stride

    In the default case, where the data_layout is `NCW`
    a data Tensor with shape `(batch_size, channels, width)`,
    to produce an output Tensor.

    The ceil_mode is used to take ceil or floor while computing out shape.
    count_include_pad indicates including or excluding padded input values in computation.
    This operator accepts data layout specification.

    Parameters
    ----------
    data : relax.Expr
        The input data to the operator.

    pool_size : Union[int, Tuple[int]]
        The size of window for pooling. It is required to have length is 1.

    strides : Union[int, Tuple[int]]
        The strides of pooling. It is required to have length is 1.

    padding : Union[int, Tuple[int, int]]
        The padding for pooling. It is required to have length either 1 or 2.

    dilation : Union[int, Tuple[int]]
        The dilation of pooling. It is required to have length is 1.

    ceil_mode : bool
        A boolean indicating if use ceil or floor to compute the output shape.
        By using ceil, every element in the input tensor will be covered by a sliding window.

    count_include_pad : bool, optional
        To include padding to compute the average.

    layout : str
        Layout of the input.

    out_layout : Optional[str]
        Layout of the output. If not specified, it is the same as data_layout

    Returns
    -------
    result : Expr
        The computed result.
    """
    if isinstance(pool_size, int):
        pool_size = (pool_size,)
    if isinstance(strides, int):
        strides = (strides,)
    if isinstance(dilation, int):
        dilation = (dilation,)
    if isinstance(padding, int):
        padding = (padding, padding)
    return _ffi_api.avg_pool1d(  # type: ignore
        data,
        pool_size,
        strides,
        padding,
        dilation,
        ceil_mode,
        count_include_pad,
        layout,
        out_layout,
    )


def avg_pool2d(
    data: Expr,
    pool_size: Union[int, Tuple[int, int]] = (1, 1),
    strides: Union[int, Tuple[int, int]] = (1, 1),
    padding: Union[int, Tuple[int, ...]] = (0, 0),
    dilation: Union[int, Tuple[int, int]] = (1, 1),
    ceil_mode: bool = False,
    count_include_pad: bool = False,
    layout: str = "NCHW",
    out_layout: Optional[str] = None,
) -> Expr:
    r"""2D average pooling operator.

    This operator takes data as input and does 2D avarage value calculation
    with in pool_size sized window by striding defined by stride.

    In the default case, where the data_layout is `NCHW`
    a data Tensor with shape `(batch_size, in_channels, height, width)`,
    to produce an output Tensor with the following rule:

    with data of shape (b, c, h, w) and pool_size (kh, kw)

    .. math::

        \mbox{out}(b, c, y, x)  = \frac{1}{kh * kw} \sum_{m=0, \ldots, kh-1}
            \sum_{n=0, \ldots, kw-1}
            \mbox{data}(b, c, \mbox{stride}[0] * y + m, \mbox{stride}[1] * x + n)

    Padding is applied to data before the computation.
    ceil_mode is used to take ceil or floor while computing out shape.
    This operator accepts data layout specification.

    Parameters
    ----------
    data : relax.Expr
        The input data to the operator.

    pool_size : Union[int, Tuple[int, int]]
        The size of window for pooling. It is required to have length either 1 or 2.

    strides : Union[int, Tuple[int, int]]
        The strides of pooling. It is required to have length either 1 or 2.

    padding : Union[int, Tuple[int, ...]]
        The padding for pooling. It is required to have length either 1, 2 or 4.

    dilation : Union[int, Tuple[int, int]]
        The dilation of pooling. It is required to have length either 1 or 2.

    ceil_mode : bool
        A boolean indicating if use ceil or floor to compute the output shape.
        By using ceil, every element in the input tensor will be covered by a sliding window.

    count_include_pad : bool, optional
        To include padding to compute the average.

    layout : str
        Layout of the input.

    out_layout : Optional[str]
        Layout of the output. If not specified, it is the same as data_layout

    Returns
    -------
    result : Expr
        The computed result.
    """
    if isinstance(pool_size, int):
        pool_size = (pool_size, pool_size)
    if isinstance(strides, int):
        strides = (strides, strides)
    if isinstance(dilation, int):
        dilation = (dilation, dilation)
    if isinstance(padding, int):
        padding = (padding, padding, padding, padding)
    return _ffi_api.avg_pool2d(  # type: ignore
        data,
        pool_size,
        strides,
        padding,
        dilation,
        ceil_mode,
        count_include_pad,
        layout,
        out_layout,
    )


def avg_pool3d(
    data: Expr,
    pool_size: Union[int, Tuple[int, int]] = (1, 1, 1),
    strides: Union[int, Tuple[int, int]] = (1, 1, 1),
    padding: Union[int, Tuple[int, ...]] = (0, 0, 0),
    dilation: Union[int, Tuple[int, int]] = (1, 1, 1),
    ceil_mode: bool = False,
    count_include_pad: bool = True,
    layout: str = "NCDHW",
    out_layout: Optional[str] = None,
) -> Expr:
    r"""2D average pooling operator.

    This operator takes data as input and does 3D average value calculation
    with in pool_size sized window by striding defined by stride


    In the default case, where the data_layout is `NCDHW`
    a data Tensor with shape `(batch_size, channels, depth, height, width)`,
    to produce an output Tensor.

    The ceil_mode is used to take ceil or floor while computing out shape.
    count_include_pad indicates including or excluding padded input values in computation.
    This operator accepts data layout specification.

    Parameters
    ----------
    data : relax.Expr
        The input data to the operator.

    pool_size : Union[int, Tuple[int, int, int]]
        The size of window for pooling. It is required to have length either 1 or 3.

    strides : Union[int, Tuple[int, int, int]]
        The strides of pooling. It is required to have length either 1 or 3.

    padding : Union[int, Tuple[int, ...]]
        The padding for pooling. It is required to have length either 1, 3 or 6.

    dilation : Union[int, Tuple[int, int, int]]
        The dilation of pooling. It is required to have length either 1 or 3.

    ceil_mode : bool
        A boolean indicating if use ceil or floor to compute the output shape.
        By using ceil, every element in the input tensor will be covered by a sliding window.

    count_include_pad : bool, optional
        To include padding to compute the average.

    layout : str
        Layout of the input.

    out_layout : Optional[str]
        Layout of the output. If not specified, it is the same as data_layout

    Returns
    -------
    result : Expr
        The computed result.
    """
    if isinstance(pool_size, int):
        pool_size = (pool_size, pool_size, pool_size)
    if isinstance(strides, int):
        strides = (strides, strides, strides)
    if isinstance(dilation, int):
        dilation = (dilation, dilation, dilation)
    if isinstance(padding, int):
        padding = (padding, padding, padding, padding, padding, padding)

    return _ffi_api.avg_pool3d(  # type: ignore
        data,
        pool_size,
        strides,
        padding,
        dilation,
        ceil_mode,
        count_include_pad,
        layout,
        out_layout,
    )


def adaptive_avg_pool1d(
    data: Expr,
    output_size: Optional[Union[int, Tuple[int]]] = None,
    layout: str = "NCW",
    out_layout: Optional[str] = None,
) -> Expr:
    r"""1D adaptive average pooling operator. This operator is experimental.

    This operator takes data as input and does 1D average value calculation
    across each window represented by W.


    In the default case, where the data_layout is `NCW`
    a data Tensor with shape `(batch_size, in_channels, width)`,
    to produce an output Tensor with shape
    (batch_size, in_channels, output_width).

    The pooling kernel and stride sizes are automatically chosen for
    desired output sizes.

    For output_size:
        If this argument is not provided, input height and width will be used
        as output width.

        If a single integer is provided for output_size, the output size is
        (N x C x output_size) for any input (NCW).

    Parameters
    ----------
    data : relax.Expr
        The input data to the operator.

    output_size : Optional[Union[int, Tuple[int, int]]]
        Output height and width.
        If not specified, it will be the same as the input height and width.
        If specified, it is required to have length either 1 or 2.

    layout : str
        Layout of the input.

    out_layout : Optional[str]
        Layout of the output. If not specified, it is the same as data_layout

    Returns
    -------
    result : relax.Expr
        The computed result.
    """
    if isinstance(output_size, int):
        output_size = (output_size,)
    return _ffi_api.adaptive_avg_pool1d(data, output_size, layout, out_layout)  # type: ignore


def adaptive_avg_pool2d(
    data: Expr,
    output_size: Optional[Union[int, Tuple[int, int]]] = None,
    layout: str = "NCHW",
    out_layout: Optional[str] = None,
) -> Expr:
    r"""2D adaptive average pooling operator. This operator is experimental.

    This operator takes data as input and does 2D average value calculation
    across each window represented by WxH.


    In the default case, where the data_layout is `NCHW`
    a data Tensor with shape `(batch_size, in_channels, height, width)`,
    to produce an output Tensor with shape
    (batch_size, in_channels, output_height, output_width).

    The pooling kernel and stride sizes are automatically chosen for
    desired output sizes.

    For output_size:
        If this argument is not provided, input height and width will be used
        as output height and width.

        If a single integer is provided for output_size, the output size is
        (N x C x output_size x output_size) for any input (NCHW).

        If a tuple of integers (height, width) are provided for output_size,
        the output size is (N x C x height x width) for any input (NCHW).

    Parameters
    ----------
    data : relax.Expr
        The input data to the operator.

    output_size : Optional[Union[int, Tuple[int, int]]]
        Output height and width.
        If not specified, it will be the same as the input height and width.
        If specified, it is required to have length either 1 or 2.

    layout : str
        Layout of the input.

    out_layout : Optional[str]
        Layout of the output. If not specified, it is the same as data_layout

    Returns
    -------
    result : relax.Expr
        The computed result.
    """
    if isinstance(output_size, int):
        output_size = (output_size, output_size)
    return _ffi_api.adaptive_avg_pool2d(data, output_size, layout, out_layout)  # type: ignore


def adaptive_avg_pool3d(
    data: Expr,
    output_size: Optional[Union[int, Tuple[int, int]]] = None,
    layout: str = "NCDHW",
    out_layout: Optional[str] = None,
) -> Expr:
    r"""3D adaptive average pooling operator. This operator is experimental.

    This operator takes data as input and does 3D average value calculation
    across each window represented by WxH.


    In the default case, where the data_layout is `NCDHW`
    a data Tensor with shape `(batch_size, in_channels, depth, height, width)`,
    to produce an output Tensor with shape
    (batch_size, in_channels, output_depth, output_height, output_width).

    The pooling kernel and stride sizes are automatically chosen for
    desired output sizes.

    For output_size:
        If this argument is not provided, input depth, height and width will be used
        as output depth, height and width.

        If a single integer is provided for output_size, the output size is
        (N x C x output_size x output_size x output_size) for any input (NCDHW).

        If a tuple of integers (depth, height, width) are provided for output_size,
        the output size is (N x C x depth x height x width) for any input (NCDHW).

    Parameters
    ----------
    data : relax.Expr
        The input data to the operator.

    output_size : Optional[Union[int, Tuple[int, int]]]
        Output height and width.
        If not specified, it will be the same as the input height and width.
        If specified, it is required to have length either 1 or 3.

    layout : str
        Layout of the input.

    out_layout : Optional[str]
        Layout of the output. If not specified, it is the same as data_layout

    Returns
    -------
    result : relax.Expr
        The computed result.
    """
    if isinstance(output_size, int):
        output_size = (output_size, output_size, output_size)
    return _ffi_api.adaptive_avg_pool3d(data, output_size, layout, out_layout)  # type: ignore


def relu(data: Expr) -> Expr:
    r"""Rectified linear unit.

    .. math::
        \text{ReLU}(x) = \max(x, 0)

    Parameters
    ----------
    data : relax.Expr
        The input data

    Returns
    -------
    result : relax.Expr
        The computed result.
    """
    return _ffi_api.relu(data)  # type: ignore


def relu6(data: Expr) -> Expr:
    r"""ReLU6 activation function.

    .. math::
        \text{ReLU6}(x) = \min(\max(x, 0), 6)

    Parameters
    ----------
    data : relax.Expr
        The input data

    Returns
    -------
    result : relax.Expr
        The computed result.
    """
    return relax.op.clip(data, 0, 6)


def leakyrelu(data: Expr, alpha: float = 0.01) -> Expr:
    """Rectified linear unit.

    .. math::
        text{LeakyReLU, negative_slope}(x) = max(x, 0) + negative_slope * min(x, 0)

    Parameters
    ----------
    data : relax.Expr
        The input data

    alpha: float
        Controls the angle of the negative slope, used for nagative inputs.
        Default value is 0.01

    Returns
    -------
    result : relax.Expr
        The computed result.
    """
    return _ffi_api.leakyrelu(data, alpha)  # type: ignore


def gelu(data: Expr) -> Expr:
    r"""Gaussian Error Linear Units function

    .. math::
        \text{GeLU}(x) = 0.5 * x * (1 + \text{erf}(x * 0.5**0.5))

    where :math:`erf` is the Gauss Error function.

    Parameters
    ----------
    data : relax.Expr
        The input data

    Returns
    -------
    result : relax.Expr
        The computed result.

    Note
    ----
    The input tensor is required to have float dtype
    """
    return _ffi_api.gelu(data)  # type: ignore


def gelu_tanh(data: Expr) -> Expr:
    r"""Gaussian Error Linear Units function with tanh approximation

    .. math::
        \text{GELU}(x) = 0.5 * x * (1 + \text{Tanh}(\sqrt(2 / \pi) * (x + 0.044715 * x^3)))

    Parameters
    ----------
    data : relax.Expr
        The input data

    Returns
    -------
    result : relax.Expr
        The computed result.

    Note
    ----
    The input tensor is required to have float dtype
    """
    return _ffi_api.gelu_tanh(data)  # type: ignore


def selu(data: Expr) -> Expr:
    r"""Scaled Exponential Linear Unit (SELU).

    .. math::
        \text{SELU}(x) = \lambda \begin{cases}
            x & \text{if } x > 0 \\
            \alpha (e^x - 1) & \text{if } x \leq 0
        \end{cases}

    where :math:`\lambda \approx 1.0507` and :math:`\alpha \approx 1.6733`.

    Parameters
    ----------
    data : relax.Expr
        The input data.

    Returns
    -------
    result : relax.Expr
        The computed result.
    """
    return _ffi_api.selu(data)


def silu(data: Expr) -> Expr:
    r"""Sigmoid Linear Unit function

    .. math::
        \text{SiLU}(x) = x * \text{sigmoid}(x)

    Parameters
    ----------
    data : relax.Expr
        The input data

    Returns
    -------
    result : relax.Expr
        The computed result.

    Note
    ----
    The input tensor is required to have float dtype
    """
    return _ffi_api.silu(data)  # type: ignore


def softmax(data: Expr, axis: int = -1) -> Expr:
    r"""Computes softmax.

    .. math:: \text{softmax}(x)_i = \frac{\exp(x_i)}{\sum_j \exp(x_j)}

    Parameters
    ----------
    data: relax.Expr
        The input data to the operator.

    axis: int
        The axis to sum over when computing softmax.
        If not specified, it is by default the last axis of the input tensor.
        Supports negative indexing.

    Returns
    -------
    result : relax.Expr
        The computed result.

    Note
    ----
    The input tensor is required to have float dtype
    """
    return _ffi_api.softmax(data, axis)  # type: ignore


def softplus(data: Expr, beta: float = 1.0, threshold: float = 20.0) -> Expr:
    r"""Softplus activation function.

    .. math:: \text{Softplus}(x) = \frac{1}{\beta} \log(1 + e^{\beta x})

    Parameters
    ----------
    data : relax.Expr
        The input data.

    beta : float, optional
        Controls the smoothness of the transition. Default is 1.0.

    threshold : float, optional
        The value beyond which the function is approximated as linear
        to avoid numerical instability. Default is 20.0.

    Returns
    -------
    result : relax.Expr
        The computed result.
    """
    return _ffi_api.softplus(data, beta, threshold)


def log_softmax(data: Expr, axis: int = -1) -> Expr:
    r"""Computes log softmax.

    .. math::

        \text{log\_softmax}(x_i) = \log\left( \frac{\exp(x_i)}{\sum_j \exp(x_j)}\right)

    .. note::
        This operator can be optimized away for inference.

    Parameters
    ----------
    data: relax.Expr
        The input data to the operator.

    axis: int
        The axis to sum over when computing log softmax.
        If not specified, it is by default the last axis of the input tensor.
        Supports negative indexing.

    Returns
    -------
    result : relax.Expr
        The computed result.
    """
    return _ffi_api.log_softmax(data, axis)  # type: ignore


def prelu(data: Expr, alpha: Expr, axis: int = 1) -> Expr:
    r"""Parametric Rectified Linear Unit (PReLU).

    .. math::
        PReLU(x) = x \text{ if } x > 0 \text{ else } \alpha * x

    Parameters
    ----------
    data : relax.Expr
        The input tensor.

    alpha : relax.Expr
        The learnable slope tensor, applied channel-wise.

    axis : int
        The axis along which the `alpha` values are applied
        Default is 1 (assuming NCHW format).

    Returns
    -------
    result : relax.Expr
        The computed result.
    """
    return _ffi_api.prelu(data, alpha, axis)


def batch_norm(
    data: Expr,
    gamma: Expr,
    beta: Expr,
    moving_mean: Expr,
    moving_var: Expr,
    axis: int,
    epsilon: float = 1e-5,
    center: bool = True,
    scale: bool = True,
    momentum: float = 0.1,
    training: bool = True,
) -> Expr:
    r"""
    Batch normalization layer (Ioffe and Szegedy, 2014).

    Normalizes the input at each batch, i.e. applies a transformation
    that maintains the mean activation close to 0 and the activation
    standard deviation close to 1.

    .. math::

        data\_mean[i] = mean(data[:,i,:,...]) \\
        data\_var[i] = var(data[:,i,:,...])

    Both *mean* and *var* returns a scalar by treating the input as a vector.

    Then compute the normalized output, which has the same shape as input, as following:

    .. math::

        out[:,i,:,...] = \frac{data[:,i,:,...] - data\_mean[i]}{\sqrt{data\_var[i]+\epsilon}}
            * gamma[i] + beta[i]

    Assume the input has size *k* on axis 1, then both ``gamma`` and ``beta``
    have shape *(k,)*.

    Besides the inputs and the outputs, this operator accepts two auxiliary
    states, ``moving_mean`` and ``moving_var``, which are *k*-length
    vectors. They are global statistics for the whole dataset, which are updated by

    .. code:: python

        moving_mean = moving_mean * momentum + data_mean * (1 - momentum)
        moving_var = moving_var * momentum + data_var * (1 - momentum)

    The parameter ``axis`` specifies which axis of the input shape denotes
    the 'channel' (separately normalized groups).  The default is 1.
    Specifying -1 sets the channel axis to be the last item in the input shape.

    .. note::

        This operator has two modes:

        - Training mode.
            - Use the mean and var computed from THIS batch to normalize.
            - Update and then return the running mean and running var.

        - Inference mode.
            - Use the running_mean and running_var parameters to normalize.
            - Do not update the running mean and running var. Just return the original value.

        In the legalization stage, this operator will be legalized to the training mode by default.

        You can use tvm.relax.transform.DecomposeOpsForInference to decompose the operator, so it
        executes the inference mode computation. Similarly, use
        tvm.relax.transform.DecomposeOpsForTraining to execute the training mode computation.

    Parameters
    ----------
    data : relax.Expr
        The input data to the operator.

    gamma : relax.Expr
        The gamma scale factor.

    beta : relax.Expr
        The beta offset factor.

    moving_mean : relax.Expr
        Running mean of input.

    moving_var : relax.Expr
        Running variance of input.

    axis : int
        The axis along which the normalization is applied.

    epsilon : float
        Small float added to variance to avoid dividing by zero.

    center : bool
        Indicating if the beta offset will be added to the normalized tensor.

    scale : bool
        Indicating if the gamma scale will be multiplied.

    momentum : float
        The value used for the moving_mean and moving_var update.

    training : bool
        A boolean value to indicate whether training or in eval mode. By default.
          relax batch_norm is training mode. To transform it to inference mode,
          can use DecomposeOpsForInference.

    Returns
    -------
    result : relax.Expr
        The computed result.
    """
    return _ffi_api.batch_norm(  # type: ignore
        data, gamma, beta, moving_mean, moving_var, axis, epsilon, center, scale, momentum, training
    )


def layer_norm(
    data: Expr,
    gamma: Expr,
    beta: Expr,
    axes: Union[int, List[int]],
    epsilon: float = 1e-5,
    center: bool = True,
    scale: bool = True,
) -> Expr:
    r"""
    Layer normalization (Lei Ba and et al., 2016).
    Applies layer normalization to the n-dimensional input array.
    This operator takes an n-dimensional input array and normalizes
    the input using the given axis:

    .. math::

        out = \frac{data - mean(data, axis)}{\sqrt{var(data, axis)+\epsilon}}
            * gamma + beta

    Unlike batch normalization, the mean and var are computed along the channel dimension.

    Assume the input has size k on axis 1, then both gamma and beta have shape (k,).

    .. note::

        This operator can be optimized away for inference.

    Parameters
    ----------
    data : relax.Expr
        Input to which layer_norm will be applied.

    gamma : relax.Expr
        The gamma scale factor.

    beta : relax.Expr
        The beta offset factor.

    axes : Union[int, List[int]]
        The axes that along which the normalization is applied.

    epsilon : float
        Small float added to variance to avoid dividing by zero.

    center : bool
        Indicating if the beta offset will be added to the normalized tensor.

    scale : bool
        Indicating if the gamma scale will be multiplied.

    Returns
    -------
    result : relax.Expr
        The computed result.
    """
    if isinstance(axes, int):
        axes = [axes]
    return _ffi_api.layer_norm(data, gamma, beta, axes, epsilon, center, scale)  # type: ignore


def group_norm(
    data: Expr,
    gamma: Expr,
    beta: Expr,
    num_groups: int,
    channel_axis: int,
    axes: Union[int, List[int]],
    epsilon: float = 1e-5,
    center: bool = True,
    scale: bool = True,
) -> Expr:
    r"""
    Group normalization (Yuxin Wu and et al., 2016).
    Applies group normalization to the n-dimensional input array.
    This operator takes an n-dimensional input array. First separate the input array
    into groups along the channel axis. Then apply layer normalization to each group.

    Parameters
    ----------
    data : relax.Expr
        Input to which group_norm will be applied.

    gamma : relax.Expr
        The gamma scale factor.

    beta : relax.Expr
        The beta offset factor.

    num_groups : int
        Number of groups to separate the channels into.

    channel_axis : int
        The index of the channel axis in the input data.

    axes : Union[int, List[int]]
        The axes that along which the normalization is applied (excluding the group axis)

    epsilon : float
        Small float added to variance to avoid dividing by zero.

    center : bool
        Indicating if the beta offset will be added to the normalized tensor.

    scale : bool
        Indicating if the gamma scale will be multiplied.

    Returns
    -------
    result : relax.Expr
        The computed result.
    """
    if isinstance(axes, int):
        axes = [axes]
    return _ffi_api.group_norm(  # type: ignore
        data, gamma, beta, num_groups, channel_axis, axes, epsilon, center, scale
    )


def instance_norm(
    data: Expr,
    gamma: Expr,
    beta: Expr,
    channel_axis: int,
    axes: List[int],
    epsilon: float = 1e-5,
    center: bool = True,
    scale: bool = True,
) -> Expr:
    r"""
    Instance normalization

    Parameters
    ----------
    data : relax.Expr
        Input to which instance_norm will be applied.

    gamma : relax.Expr
        The gamma scale factor.

    beta : relax.Expr
        The beta offset factor.

    axes : Union[int, List[int]]
        The axes that along which the normalization is applied.

    epsilon : float
        Small float added to variance to avoid dividing by zero.

    center : bool
        Indicating if the beta offset will be added to the normalized tensor.

    scale : bool
        Indicating if the gamma scale will be multiplied.

    Returns
    -------
    result : relax.Expr
        The computed result.
    """
    if isinstance(axes, int):
        axes = [axes]
    return _ffi_api.instance_norm(  # type: ignore
        data,
        gamma,
        beta,
        channel_axis,
        axes,
        epsilon,
        center,
        scale,
    )


def rms_norm(
    data: Expr,
    weight: Expr,
    axes: Union[int, List[int]] = -1,
    epsilon: float = 1e-5,
) -> Expr:
    r"""
    Root mean square normalization (Biao Zhang and et al., 2019).
    Applies root mean square normalization to the n-dimensional input array.
    This operator takes an n-dimensional input array and normalizes
    the input using the given axis:

    .. math::

        out = \frac{data}{\sqrt{mean(data, axis)+\epsilon}} * weight + bias

    Parameters
    ----------
    data : relax.Expr
        Input to which rms_norm will be applied.

    weight : relax.Expr
        The scale factor.

    bias : relax.Expr
        The offset factor.

    axes : Union[int, List[int]]
        The axes that along which the normalization is applied.

    epsilon : float
        Small float added to square mean to avoid dividing by zero.

    Returns
    -------
    result : relax.Expr
        The computed result.
    """
    if isinstance(axes, int):
        axes = [axes]
    return _ffi_api.rms_norm(data, weight, axes, epsilon)  # type: ignore


def dropout(data: Expr, rate: float = 0.5) -> Expr:
    """Applies the dropout operation to the input tensor.

    During training, each element of the input is set to zero with
    probability ``p``. The whole array is scaled by ``1/(1-p)``
    to keep the expected sum of the input unchanged.

    Parameters
    ----------
    data : relax.Expr
        The input data to the operator.

    rate : float
        The probability for an element to be reset to 0.

    Returns
    -------
    result : relax.Expr
        The result of dropout, which is a tuple of two tensors.
        The first one is the original tensor and the second one is a
        mask tensor (1.0 where element not dropped, 0.0 where dropped)
    """
    return _ffi_api.dropout(data, rate)  # type: ignore


def cross_entropy_with_logits(predictions: Expr, labels: Expr) -> Expr:
    r"""CrossEntropy with logits between the predictions and labels.

    The shape of predictions and labels must be the same. And when ndim >= 2,
    the first dimension is regarded as the batch_size N. In this case the
    computed result will divide by N to perform a mean reduction.

    .. math::

        \text{cross\_entropy\_with\_logits}(x_i, y_i) = \frac{\sum_i -x_i \cdot y_i}{N}

    Parameters
    ----------
    predictions : relax.Expr
      The predictions.

    labels : relax.Expr
      The labels (the ground truth values).

    Returns
    -------
    result : relax.Expr
      The computed result.
    """
    return _ffi_api.cross_entropy_with_logits(predictions, labels)  # type: ignore


def nll_loss(
    predictions: Expr,
    targets: Expr,
    weights: Optional[Expr] = None,
    reduction: str = "mean",
    ignore_index: int = -100,
) -> Expr:
    """Negative log likelihood loss.

    `output[n, i_1, i_2, ..., i_k] = -p * w`, where
    - `p = predictions[n, t, i_1, i_2, i_k]`,
    - `t = targets[n, i_1, i_2, ..., i_k]`,
    - `w = weights[t] if t != ignore_index else 0`

    result = reduction(output)

    Parameters
    ----------
    predictions : relax.Expr
      The predictions. Should be a `(k+2)-D` Tensor with shape `(N, C, d_1, d_2, ..., d_k)` where C
      is the number of target classes.

    targets : relax.Expr
      The target value of each prediction. Should be a `(k+1)-D` Tensor with shape
      `(N, d_1, d_2, ..., d_k)`. Must be of int dtype.

    weights : Optional[relax.Expr]
      The weight of each target value. Should be a `1-D` Tensor with shape `(C,)`.
      If not specified, it is treated as if having all ones.

    reduction : str
      The reduction method to apply to the output.
      Possible values are "mean", "sum" and "none".

    ignore_index : int
      The target value to ignore.

    Returns
    -------
    result : relax.Expr
      The computed result.
    """
    return _ffi_api.nll_loss(predictions, targets, weights, reduction, ignore_index)  # type: ignore


def attention(
    query: Expr,
    key: Expr,
    value: Expr,
    bias: Optional[Expr] = None,
    scale: Optional[FloatImm] = None,
    causal_mask: Optional[str] = None,
    window_size: Optional[int] = None,
) -> Expr:
    r"""Computes fused multi head attention.

    All input tensors are of 4-D tensors with BSNH layout.

    .. math::
        FMA(Q, K, V) = \text{Softmax}(Q @ K^T) @ V

    .. note::
        The input tensor is required to have float16 dtype

    Parameters
    ----------
    query: relax.Expr
        The input query to the operator. The layout of the input query should be
        (batch_size, seq_len, num_head, head_dim).

    key: relax.Expr
        The input key to the operator. The layout of the input key should be
        (batch_size, seq_len_kv, num_head, head_dim).

    value: relax.Expr
        The input value to the operator. The layout of the input value should be
        (batch_size, seq_len_kv, num_head, head_dim_v).

    bias: Optional[Expr]
        The optional attention bias to the operator. The layout of the attention bias should be
        a 4-D tensor ending with seq_len_kv, and broadcastable to
        (batch_size, num_head, seq_len, seq_len_kv).

    scale: Optional[float]
        The scale value to be applied to the attention score, by default 1 / sqrt(head_dim).

    causal_mask: Optional[str]
        The optional causal mask, i.e. 'TopLeft' and 'BottomRight'.
        For 'TopLeft', the mask matrix is as `np.tril(*, k=0)`,
        while for 'BottomRight', the mask matrix is as `np.tril(*, k=abs(seq_len - seq_len_kv))`
        For example, with seq_len = 4, seq_len_kv = 2,
        mask for 'TopLeft':

        .. code:: python

            [[1, 0],
            [1, 1],
            [1, 1],
            [1, 1]]

        mask for 'BottomRight':

        .. code:: python

            [[1, 1],
            [1, 1],
            [1, 1],
            [1, 1]]

        with seq_len = 2, seq_len_kv = 4,
        mask for 'TopLeft':

        .. code:: python

            [[1, 0, 0, 0],
            [1, 1, 0, 0]]

        mask for 'BottomRight':

        .. code:: python

            [[1, 1, 1, 0],
            [1, 1, 1, 1]]

    window_size: Optional[int]
        The size of the window for sliding-window attention.

    Returns
    -------
    result : relax.Expr
        The computed result. The layout of the output should be
        (batch_size, seq_len, num_head, head_dim_v).
    """
    return _ffi_api.attention(
        query, key, value, bias, scale, causal_mask, window_size
    )  # type: ignore


def attention_bias(
    query: Expr,
    key: Expr,
    value: Expr,
    bias: Optional[Expr] = None,
    scale: Optional[FloatImm] = None,
    causal_mask: Optional[str] = None,
    window_size: Optional[int] = None,
) -> Expr:
    r"""Computes fused multi head attention.

    IRModule.script() transforms attention op to attention_bias which is incompatible
    with TVMScript Parser.
    The function makes TVMScript's print compatible with TVMScript's parser.

    All input tensors are of 4-D tensors with BSNH layout.

    .. math::
        FMA(Q, K, V) = \text{Softmax}(Q @ K^T) @ V

    .. note::
        The input tensor is required to have float16 dtype

    Parameters
    ----------
    query: relax.Expr
        The input query to the operator. The layout of the input query should be
        (batch_size, seq_len, num_head, head_dim).

    key: relax.Expr
        The input key to the operator. The layout of the input key should be
        (batch_size, seq_len_kv, num_head, head_dim).

    value: relax.Expr
        The input value to the operator. The layout of the input value should be
        (batch_size, seq_len_kv, num_head, head_dim_v).

    bias: Optional[Expr]
        The optional attention bias to the operator. The layout of the attention bias should be
        a 4-D tensor ending with seq_len_kv, and broadcastable to
        (batch_size, num_head, seq_len, seq_len_kv).

    scale: Optional[float]
        The scale value to be applied to the attention score, by default 1 / sqrt(head_dim).

    causal_mask: Optional[str]
        The optional causal mask, i.e. 'TopLeft' and 'BottomRight'.
        For 'TopLeft', the mask matrix is as `np.tril(*, k=0)`,
        while for 'BottomRight', the mask matrix is as `np.tril(*, k=abs(seq_len - seq_len_kv))`
        For example, with seq_len = 4, seq_len_kv = 2,
        mask for 'TopLeft':

        .. code:: python

            [[1, 0],
            [1, 1],
            [1, 1],
            [1, 1]]

        mask for 'BottomRight':

        .. code:: python

            [[1, 1],
            [1, 1],
            [1, 1],
            [1, 1]]

        with seq_len = 2, seq_len_kv = 4,
        mask for 'TopLeft':

        .. code:: python

            [[1, 0, 0, 0],
            [1, 1, 0, 0]]

        mask for 'BottomRight':

        .. code:: python

            [[1, 1, 1, 0],
            [1, 1, 1, 1]]

    window_size: Optional[int]
        The size of the window for sliding-window attention.

    Returns
    -------
    result : relax.Expr
        The computed result. The layout of the output should be
        (batch_size, seq_len, num_head, head_dim_v).
    """
    return _ffi_api.attention(
        query, key, value, bias, scale, causal_mask, window_size
    )  # type: ignore


def attention_var_len(
    queries: Expr,
    keys: Expr,
    values: Expr,
    seqstart_q: Expr,
    max_seqlen_q: Expr,
    seqstart_k: Optional[Expr] = None,
    max_seqlen_k: Optional[Expr] = None,
    scale: Optional[FloatImm] = None,
    causal_mask: Optional[str] = None,
    window_size: Optional[int] = None,
) -> Expr:
    """Computes fused multi head attention over batched sequences of variable lengths.

    Given concatenated inputs and sequence lengths information, this operator computes
    attention for all sequences more efficiently than calling the normal attention operator
    for each sequence individually.

    Parameters
    ----------
    queries: relax.Expr
        The input queries concatenated along the second axis. Its shape must be
        (1, total_seq_len, num_head, head_dim).

    keys: relax.Expr
        The input keys concatenated along the second axis. Its shape must be
        (1, total_seq_len_kv, num_head, head_dim).

    values: relax.Expr
        The input values concatenated along the second axis. Its shape must be
        (1, total_seq_len_kv, num_head, head_dim_v).

    seqstart_q: Optional[Expr]
        The cumsum of query sequence lengths, prepended with 0. Its dtype must be int32.
        For example, if the lengths of the sequences that are batched are [2, 5, 3],
        this tensor has values [0, 2, 7, 10].

    seqstart_k: Optional[Expr]
        The cumsum of key sequence lengths, prepended with 0.
        By default it is the same as seqstart_q.

    max_seqlen_q: Optional[Expr]
        The maximum query sequence length in the batch. It must be int32.

    max_seqlen_k: Optional[Expr]
        The maximum key sequence length in the batch. It must be int32.
        By default it is the same as max_seqlen_q.

    scale: Optional[float]
        The scale value to be applied to the attention score, by default 1 / sqrt(head_dim).

    causal_mask: Optional[str]
        The optional causal mask, i.e. 'TopLeft' and 'BottomRight'.
        For 'TopLeft', the mask matrix is as `np.tril(*, k=0)`,
        while for 'BottomRight', the mask matrix is as `np.tril(*, k=abs(seq_len - seq_len_kv))`
        For example, with seq_len = 4, seq_len_kv = 2,
        mask for 'TopLeft':

        .. code:: python

            [[1, 0],
            [1, 1],
            [1, 1],
            [1, 1]]

        mask for 'BottomRight':

        .. code:: python

            [[1, 1],
            [1, 1],
            [1, 1],
            [1, 1]]

        with seq_len = 2, seq_len_kv = 4,
        mask for 'TopLeft':

        .. code:: python

            [[1, 0, 0, 0],
            [1, 1, 0, 0]]

        mask for 'BottomRight':

        .. code:: python

            [[1, 1, 1, 0],
            [1, 1, 1, 1]]

    window_size: Optional[int]
        The size of the window for sliding-window attention.

    Returns
    -------
    result : relax.Expr
        The computed result with shape `(1, total_seq_len, num_head, head_dim_v)`.
    """
    if seqstart_k is None:
        seqstart_k = seqstart_q
    if max_seqlen_k is None:
        max_seqlen_k = max_seqlen_q
    return _ffi_api.attention_var_len(
        queries,
        keys,
        values,
        seqstart_q,
        seqstart_k,
        max_seqlen_q,
        max_seqlen_k,
        scale,
        causal_mask,
        window_size,
    )  # type: ignore
