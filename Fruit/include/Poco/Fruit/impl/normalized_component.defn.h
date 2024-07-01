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

#ifndef FRUIT_NORMALIZED_COMPONENT_INLINES_H
#define FRUIT_NORMALIZED_COMPONENT_INLINES_H

#include <Poco/Fruit/normalized_component.h>

#include <Poco/Fruit/component.h>
#include <Poco/Fruit/impl/util/type_info.h>

namespace Fruit {

template <typename... Params>
template <typename... FormalArgs, typename... Args>
inline NormalizedComponent<Params...>::NormalizedComponent(Component<Params...> (*getComponent)(FormalArgs...),
                                                           Args&&... args)
    : NormalizedComponent(std::move(Fruit::Component<Params...>(
                                        Fruit::createComponent().install(getComponent, std::forward<Args>(args)...))
                                        .storage),
                          Fruit::impl::MemoryPool()) {}

template <typename... Params>
inline NormalizedComponent<Params...>::NormalizedComponent(Fruit::impl::ComponentStorage&& storage,
                                                           Fruit::impl::MemoryPool memory_pool)
    : storage(std::move(storage),
              Fruit::impl::getTypeIdsForList<typename Fruit::impl::meta::Eval<Fruit::impl::meta::SetToVector(
                  typename Fruit::impl::meta::Eval<Fruit::impl::meta::ConstructComponentImpl(
                      Fruit::impl::meta::Type<Params>...)>::Ps)>>(memory_pool),
              memory_pool, Fruit::impl::NormalizedComponentStorageHolder::WithUndoableCompression()) {}

} // namespace Fruit

#endif // FRUIT_NORMALIZED_COMPONENT_INLINES_H
