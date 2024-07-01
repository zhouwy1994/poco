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

#ifndef FRUIT_CALL_WITH_TUPLE_H
#define FRUIT_CALL_WITH_TUPLE_H

#include <Poco/Fruit/impl/meta/vector.h>

namespace Poco{
namespace Fruit {
namespace impl {

template <typename IntVector, typename Result, typename ArgsTuple>
struct CallWithTupleHelper;

template <typename... Ints, typename Result, typename... Args>
struct CallWithTupleHelper<Poco::Fruit::impl::meta::Vector<Ints...>, Result, std::tuple<Args...>> {
  Result operator()(Result (*fun)(Args...), std::tuple<Args...> args) {
    // This parameter *is* used, but when the tuple is empty some compilers report is as unused.
    (void)args;
    return fun(std::get<Poco::Fruit::impl::meta::getIntValue<Ints>()>(args)...);
  }
};

template <typename Result, typename... Args>
inline Result callWithTuple(Result (*fun)(Args...), std::tuple<Args...> args) {
  using IntVector =
      Poco::Fruit::impl::meta::Eval<Poco::Fruit::impl::meta::GenerateIntSequence(Poco::Fruit::impl::meta::Int<sizeof...(Args)>)>;
  return CallWithTupleHelper<IntVector, Result, std::tuple<Args...>>()(fun, args);
}
}
}
}

#endif // FRUIT_CALL_WITH_TUPLE_H
