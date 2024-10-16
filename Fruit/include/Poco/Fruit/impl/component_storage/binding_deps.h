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

#ifndef FRUIT_BINDING_DEPS_H
#define FRUIT_BINDING_DEPS_H

#include <Poco/Fruit/impl/util/type_info.h>

namespace Poco{
namespace Fruit {
namespace impl {

struct BindingDeps {
  // A C-style array of deps
  const TypeId* deps;

  // The size of the above array.
  std::size_t num_deps;
};

template <typename Deps>
const BindingDeps* getBindingDeps();

} // namespace impl
} // namespace Fruit
} // namespace Poco

#include <Poco/Fruit/impl/component_storage/binding_deps.defn.h>

#endif // FRUIT_BINDING_DEPS_H
