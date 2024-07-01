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

#ifndef FRUIT_COMPONENT_DEFN_H
#define FRUIT_COMPONENT_DEFN_H

#include <Poco/Fruit/component.h>

#include <Poco/Fruit/impl/component_storage/component_storage.h>
#include <Poco/Fruit/impl/injection_errors.h>
#include <Poco/Fruit/impl/component_install_arg_checks.h>

#include <memory>

namespace Fruit {

namespace impl {
namespace meta {
// This is a helper class used in the implementation of Component and PartialComponent.
// It's in Fruit::impl::meta so that we don't need to qualify everything with Fruit::impl::meta.
template <typename... PreviousBindings>
struct OpForComponent {
  template <typename Comp>
  using ConvertTo = Eval<Call(ReverseComposeFunctors(Id<ComponentFunctor(ConvertComponent, Comp)>,
                                                     ProcessDeferredBindings, Id<ProcessBinding(PreviousBindings)>...),
                              ConstructComponentImpl())>;

  template <typename Binding>
  using AddBinding =
      Eval<Call(ReverseComposeFunctors(Id<ProcessBinding(Binding)>, Id<ProcessBinding(PreviousBindings)>...),
                ConstructComponentImpl())>;
};
} // namespace meta
} // namespace impl

template <typename... Params>
template <typename... Bindings>
inline Component<Params...>::Component(PartialComponent<Bindings...>&& partial_component) noexcept : storage() {

  (void)typename Fruit::impl::meta::CheckIfError<Comp>::type();

  using Op = typename Fruit::impl::meta::OpForComponent<Bindings...>::template ConvertTo<Comp>;
  (void)typename Fruit::impl::meta::CheckIfError<Op>::type();

#if !FRUIT_NO_LOOP_CHECK
  (void)typename Fruit::impl::meta::CheckIfError<
      Fruit::impl::meta::Eval<Fruit::impl::meta::CheckNoLoopInDeps(typename Op::Result)>>::type();
#endif // !FRUIT_NO_LOOP_CHECK

  std::size_t num_entries = partial_component.storage.numBindings() + Op().numEntries();
  Fruit::impl::FixedSizeVector<Fruit::impl::ComponentStorageEntry> entries(num_entries);

  Op()(entries);

  // addBindings may modify the storage member of PartialComponent.
  // Therefore, it should not be used after this operation.
  partial_component.storage.addBindings(entries);

  // TODO: re-enable this check somehow.
  // component.component.already_converted_to_component = true;

  FruitAssert(entries.size() == num_entries);

  storage = Fruit::impl::ComponentStorage(std::move(entries));
}

inline PartialComponent<> createComponent() {
  return {{}};
}

template <typename... Bindings>
template <typename AnnotatedI, typename AnnotatedC>
inline PartialComponent<Fruit::impl::Bind<AnnotatedI, AnnotatedC>, Bindings...> PartialComponent<Bindings...>::bind() {
  using Op = OpFor<Fruit::impl::Bind<AnnotatedI, AnnotatedC>>;
  (void)typename Fruit::impl::meta::CheckIfError<Op>::type();

  return {{storage}};
}

template <typename... Bindings>
template <typename AnnotatedSignature>
inline PartialComponent<Fruit::impl::RegisterConstructor<AnnotatedSignature>, Bindings...>
PartialComponent<Bindings...>::registerConstructor() {
  using Op = OpFor<Fruit::impl::RegisterConstructor<AnnotatedSignature>>;
  (void)typename Fruit::impl::meta::CheckIfError<Op>::type();

  return {{storage}};
}

template <typename... Bindings>
template <typename C>
inline PartialComponent<Fruit::impl::BindInstance<C, C>, Bindings...>
PartialComponent<Bindings...>::bindInstance(C& instance) {
  using Op = OpFor<Fruit::impl::BindInstance<C, C>>;
  (void)typename Fruit::impl::meta::CheckIfError<Op>::type();
  return {{storage, instance}};
}

template <typename... Bindings>
template <typename C>
inline PartialComponent<Fruit::impl::BindConstInstance<C, C>, Bindings...>
PartialComponent<Bindings...>::bindInstance(const C& instance) {
  using Op = OpFor<Fruit::impl::BindConstInstance<C, C>>;
  (void)typename Fruit::impl::meta::CheckIfError<Op>::type();
  return {{storage, instance}};
}

template <typename... Bindings>
template <typename AnnotatedC, typename C>
inline PartialComponent<Fruit::impl::BindInstance<AnnotatedC, C>, Bindings...>
PartialComponent<Bindings...>::bindInstance(C& instance) {
  using Op = OpFor<Fruit::impl::BindInstance<AnnotatedC, C>>;
  (void)typename Fruit::impl::meta::CheckIfError<Op>::type();
  return {{storage, instance}};
}

template <typename... Bindings>
template <typename AnnotatedC, typename C>
inline PartialComponent<Fruit::impl::BindConstInstance<AnnotatedC, C>, Bindings...>
PartialComponent<Bindings...>::bindInstance(const C& instance) {
  using Op = OpFor<Fruit::impl::BindConstInstance<AnnotatedC, C>>;
  (void)typename Fruit::impl::meta::CheckIfError<Op>::type();
  return {{storage, instance}};
}

template <typename... Bindings>
template <typename Lambda>
inline PartialComponent<Fruit::impl::RegisterProvider<Lambda>, Bindings...>
PartialComponent<Bindings...>::registerProvider(Lambda) {
  using Op = OpFor<Fruit::impl::RegisterProvider<Lambda>>;
  (void)typename Fruit::impl::meta::CheckIfError<Op>::type();
  return {{storage}};
}

template <typename... Bindings>
template <typename AnnotatedSignature, typename Lambda>
inline PartialComponent<Fruit::impl::RegisterProvider<AnnotatedSignature, Lambda>, Bindings...>
PartialComponent<Bindings...>::registerProvider(Lambda) {
  using Op = OpFor<Fruit::impl::RegisterProvider<AnnotatedSignature, Lambda>>;
  (void)typename Fruit::impl::meta::CheckIfError<Op>::type();
  return {{storage}};
}

template <typename... Bindings>
template <typename AnnotatedI, typename AnnotatedC>
inline PartialComponent<Fruit::impl::AddMultibinding<AnnotatedI, AnnotatedC>, Bindings...>
PartialComponent<Bindings...>::addMultibinding() {
  using Op = OpFor<Fruit::impl::AddMultibinding<AnnotatedI, AnnotatedC>>;
  (void)typename Fruit::impl::meta::CheckIfError<Op>::type();

  return {{storage}};
}

template <typename... Bindings>
template <typename C>
inline PartialComponent<Fruit::impl::AddInstanceMultibinding<C>, Bindings...>
PartialComponent<Bindings...>::addInstanceMultibinding(C& instance) {
  using Op = Fruit::impl::meta::Eval<Fruit::impl::meta::CheckNormalizedTypes(
      Fruit::impl::meta::Vector<Fruit::impl::meta::Type<C>>)>;
  (void)typename Fruit::impl::meta::CheckIfError<Op>::type();

  return {{storage, instance}};
}

template <typename... Bindings>
template <typename AnnotatedC, typename C>
inline PartialComponent<Fruit::impl::AddInstanceMultibinding<AnnotatedC>, Bindings...>
PartialComponent<Bindings...>::addInstanceMultibinding(C& instance) {
  using Op = Fruit::impl::meta::Eval<Fruit::impl::meta::CheckNormalizedTypes(
      Fruit::impl::meta::Vector<Fruit::impl::meta::Type<C>>)>;
  (void)typename Fruit::impl::meta::CheckIfError<Op>::type();
  return {{storage, instance}};
}

template <typename... Bindings>
template <typename C>
inline PartialComponent<Fruit::impl::AddInstanceVectorMultibindings<C>, Bindings...>
PartialComponent<Bindings...>::addInstanceMultibindings(std::vector<C>& instances) {
  using Op = Fruit::impl::meta::Eval<Fruit::impl::meta::CheckNormalizedTypes(
      Fruit::impl::meta::Vector<Fruit::impl::meta::Type<C>>)>;
  (void)typename Fruit::impl::meta::CheckIfError<Op>::type();
  return {{storage, instances}};
}

template <typename... Bindings>
template <typename AnnotatedC, typename C>
inline PartialComponent<Fruit::impl::AddInstanceVectorMultibindings<AnnotatedC>, Bindings...>
PartialComponent<Bindings...>::addInstanceMultibindings(std::vector<C>& instances) {
  using Op = Fruit::impl::meta::Eval<Fruit::impl::meta::CheckNormalizedTypes(
      Fruit::impl::meta::Vector<Fruit::impl::meta::Type<C>>)>;
  (void)typename Fruit::impl::meta::CheckIfError<Op>::type();

  return {{storage, instances}};
}

template <typename... Bindings>
template <typename Lambda>
inline PartialComponent<Fruit::impl::AddMultibindingProvider<Lambda>, Bindings...>
PartialComponent<Bindings...>::addMultibindingProvider(Lambda) {
  using Op = OpFor<Fruit::impl::AddMultibindingProvider<Lambda>>;
  (void)typename Fruit::impl::meta::CheckIfError<Op>::type();

  return {{storage}};
}

template <typename... Bindings>
template <typename AnnotatedSignature, typename Lambda>
inline PartialComponent<Fruit::impl::AddMultibindingProvider<AnnotatedSignature, Lambda>, Bindings...>
PartialComponent<Bindings...>::addMultibindingProvider(Lambda) {
  using Op = OpFor<Fruit::impl::AddMultibindingProvider<AnnotatedSignature, Lambda>>;
  (void)typename Fruit::impl::meta::CheckIfError<Op>::type();

  return {{storage}};
}

template <typename... Bindings>
template <typename DecoratedSignature, typename Lambda>
inline PartialComponent<Fruit::impl::RegisterFactory<DecoratedSignature, Lambda>, Bindings...>
PartialComponent<Bindings...>::registerFactory(Lambda) {
  using Op = OpFor<Fruit::impl::RegisterFactory<DecoratedSignature, Lambda>>;
  (void)typename Fruit::impl::meta::CheckIfError<Op>::type();

  return {{storage}};
}

template <typename... Bindings>
inline PartialComponent<Bindings...>::PartialComponent(Fruit::impl::PartialComponentStorage<Bindings...> storage)
    : storage(std::move(storage)) {}

template <typename... Bindings>
template <typename... OtherComponentParams, typename... FormalArgs, typename... Args>
inline PartialComponent<Fruit::impl::InstallComponent<Fruit::Component<OtherComponentParams...>(FormalArgs...)>,
                        Bindings...>
PartialComponent<Bindings...>::install(Fruit::Component<OtherComponentParams...> (*getComponent)(FormalArgs...),
                                       Args&&... args) {
  using IntCollector = int[];
  (void)IntCollector{0, Fruit::impl::checkAcceptableComponentInstallArg<FormalArgs>()...};

  using Op = OpFor<Fruit::impl::InstallComponent<Fruit::Component<OtherComponentParams...>(FormalArgs...)>>;
  (void)typename Fruit::impl::meta::CheckIfError<Op>::type();

  std::tuple<FormalArgs...> args_tuple{std::forward<Args>(args)...};

  return {{storage, getComponent, std::move(args_tuple)}};
}

template <typename... Bindings>
template <typename... ComponentFunctions>
inline PartialComponent<Fruit::impl::InstallComponentFunctions<ComponentFunctions...>, Bindings...>
PartialComponent<Bindings...>::installComponentFunctions(ComponentFunctions... componentFunctions) {

  using Op = OpFor<Fruit::impl::InstallComponentFunctions<ComponentFunctions...>>;
  (void)typename Fruit::impl::meta::CheckIfError<Op>::type();

  std::tuple<ComponentFunctions...> component_functions_tuple{std::move(componentFunctions)...};

  return {{storage, std::move(component_functions_tuple)}};
}

template <typename... Bindings>
template <typename... OtherComponentParams, typename... FormalArgs, typename... Args>
inline typename PartialComponent<Bindings...>::template PartialComponentWithReplacementInProgress<
    Fruit::Component<OtherComponentParams...>, FormalArgs...>
PartialComponent<Bindings...>::replace(Fruit::Component<OtherComponentParams...> (*getReplacedComponent)(FormalArgs...),
                                       Args&&... args) {
  using IntCollector = int[];
  (void)IntCollector{0, Fruit::impl::checkAcceptableComponentInstallArg<FormalArgs>()...};

  std::tuple<FormalArgs...> args_tuple{std::forward<Args>(args)...};

  return {{storage, getReplacedComponent, std::move(args_tuple)}};
}

template <typename... Bindings>
template <typename OtherComponent, typename... GetReplacedComponentFormalArgs>
template <typename... GetReplacementComponentFormalArgs, typename... Args>
inline PartialComponent<Fruit::impl::ReplaceComponent<OtherComponent(GetReplacedComponentFormalArgs...),
                                                      OtherComponent(GetReplacementComponentFormalArgs...)>,
                        Bindings...>
PartialComponent<Bindings...>::
    PartialComponentWithReplacementInProgress<OtherComponent, GetReplacedComponentFormalArgs...>::with(
        OtherComponent (*getReplacementComponent)(GetReplacementComponentFormalArgs...), Args&&... args) {
  using IntCollector = int[];
  (void)IntCollector{0, Fruit::impl::checkAcceptableComponentInstallArg<GetReplacementComponentFormalArgs>()...};

  std::tuple<GetReplacementComponentFormalArgs...> args_tuple{std::forward<Args>(args)...};

  return {{storage, getReplacementComponent, std::move(args_tuple)}};
}

} // namespace Fruit

#endif // FRUIT_COMPONENT_DEFN_H
