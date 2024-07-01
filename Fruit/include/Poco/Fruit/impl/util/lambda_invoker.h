/*
 * Copyright 2014 Google Inc. All rights reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#ifndef FRUIT_LAMBDA_INVOKER_H
#define FRUIT_LAMBDA_INVOKER_H

#include <Poco/Fruit/impl/fruit-config.h>
#include <Poco/Fruit/impl/injection_errors.h>
#include <Poco/Fruit/impl/meta/errors.h>
#include <Poco/Fruit/impl/meta/metaprogramming.h>
#include <Poco/Fruit/impl/meta/signatures.h>
#include <Poco/Fruit/impl/meta/wrappers.h>

#include <cstddef>
#include <functional>
#include <type_traits>

namespace Poco{
namespace Fruit {
namespace impl {

template <typename T>
struct SafeAlignmentOf {
  constexpr static const std::size_t value = alignof(T);
};

template <typename T, typename... Args>
struct SafeAlignmentOf<T(Args...)> {
  constexpr static const std::size_t value = alignof(int);
};

class LambdaInvoker {
public:
  template <typename F, typename... Args>
  FRUIT_ALWAYS_INLINE static auto invoke(Args&&... args) 
      -> decltype(std::declval<const F&>()(std::declval<Args>()...)) {
    // We reinterpret-cast a char[] to avoid de-referencing nullptr, which would technically be
    // undefined behavior (even though we would not access any data there anyway).
    // Sharing this buffer for different types F would also be undefined behavior since we'd break
    // strict aliasing between those types.
    alignas(SafeAlignmentOf<F>::value) static char buf[1];

    FruitStaticAssert(Poco::Fruit::impl::meta::IsEmpty(Poco::Fruit::impl::meta::Type<F>));
    FruitStaticAssert(Poco::Fruit::impl::meta::IsTriviallyCopyable(Poco::Fruit::impl::meta::Type<F>));
    // Since `F' is empty, a valid value of type F is already stored at the beginning of buf.
    F* f = reinterpret_cast<F*>((char*)buf);
    return (*f)(std::forward<Args>(args)...);
  }
};

} // namespace impl
} // namespace Fruit
} // namespace Poco

#endif // FRUIT_LAMBDA_INVOKER_H
