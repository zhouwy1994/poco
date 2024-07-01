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

#ifndef FRUIT_INJECTOR_DEFN_H
#define FRUIT_INJECTOR_DEFN_H

#include <Poco/Fruit/component.h>

// Redundant, but makes KDevelop happy.
#include <Poco/Fruit/injector.h>

namespace Poco{
namespace Fruit {

template <typename... P>
template <typename... FormalArgs, typename... Args>
inline Injector<P...>::Injector(Component<P...> (*getComponent)(FormalArgs...), Args&&... args) {
  Component<P...> component = Poco::Fruit::createComponent().install(getComponent, std::forward<Args>(args)...);

  Poco::Fruit::impl::MemoryPool memory_pool;
  using exposed_types_t = std::vector<Poco::Fruit::impl::TypeId, Poco::Fruit::impl::ArenaAllocator<Poco::Fruit::impl::TypeId>>;
  exposed_types_t exposed_types =
      exposed_types_t(std::initializer_list<Poco::Fruit::impl::TypeId>{Poco::Fruit::impl::getTypeId<P>()...},
                      Poco::Fruit::impl::ArenaAllocator<Poco::Fruit::impl::TypeId>(memory_pool));
  storage = std::unique_ptr<Poco::Fruit::impl::InjectorStorage>(
      new Poco::Fruit::impl::InjectorStorage(std::move(component.storage), exposed_types, memory_pool));
}

namespace impl {
namespace meta {

template <typename... P>
struct InjectorImplHelper {

  // This performs all checks needed in the constructor of Injector that takes NormalizedComponent.
  template <typename NormalizedComp, typename Comp>
  struct CheckConstructionFromNormalizedComponent {
    using Op = InstallComponent(Comp, NormalizedComp);

    // The calculation of MergedComp will also do some checks, e.g. multiple bindings for the same type.
    using MergedComp = GetResult(Op);

    using TypesNotProvided = SetDifference(RemoveConstFromTypes(Vector<Type<P>...>), GetComponentPs(MergedComp));
    using MergedCompRs = SetDifference(GetComponentRsSuperset(MergedComp), GetComponentPs(MergedComp));

    using type = Eval<If(
        Not(IsEmptySet(GetComponentRsSuperset(Comp))),
        ConstructErrorWithArgVector(ComponentWithRequirementsInInjectorErrorTag,
                                    SetToVector(GetComponentRsSuperset(Comp))),
        If(Not(IsEmptySet(MergedCompRs)),
           ConstructErrorWithArgVector(UnsatisfiedRequirementsInNormalizedComponentErrorTag, SetToVector(MergedCompRs)),
           If(Not(IsContained(VectorToSetUnchecked(RemoveConstFromTypes(Vector<Type<P>...>)),
                              GetComponentPs(MergedComp))),
              ConstructErrorWithArgVector(TypesInInjectorNotProvidedErrorTag, SetToVector(TypesNotProvided)),
              If(Not(IsContained(VectorToSetUnchecked(RemoveConstTypes(Vector<Type<P>...>)),
                                 GetComponentNonConstRsPs(MergedComp))),
                 ConstructErrorWithArgVector(
                     TypesInInjectorProvidedAsConstOnlyErrorTag,
                     SetToVector(SetDifference(VectorToSetUnchecked(RemoveConstTypes(Vector<Type<P>...>)),
                                               GetComponentNonConstRsPs(MergedComp)))),
                 None))))>;
  };

  template <typename T>
  struct CheckGet {
    using Comp = ConstructComponentImpl(Type<P>...);

    using type = Eval<PropagateError(CheckInjectableType(RemoveAnnotations(Type<T>)),
                                     If(Not(IsInSet(NormalizeType(Type<T>), GetComponentPs(Comp))),
                                        ConstructError(TypeNotProvidedErrorTag, Type<T>),
                                        If(And(TypeInjectionRequiresNonConstBinding(Type<T>),
                                               Not(IsInSet(NormalizeType(Type<T>), GetComponentNonConstRsPs(Comp)))),
                                           ConstructError(TypeProvidedAsConstOnlyErrorTag, Type<T>), None)))>;
  };
};

} // namespace meta
} // namespace impl

template <typename... P>
template <typename... NormalizedComponentParams, typename... ComponentParams, typename... FormalArgs, typename... Args>
inline Injector<P...>::Injector(const NormalizedComponent<NormalizedComponentParams...>& normalized_component,
                                Component<ComponentParams...> (*getComponent)(FormalArgs...), Args&&... args) {
  Component<ComponentParams...> component = Poco::Fruit::createComponent().install(getComponent, std::forward<Args>(args)...);

  Poco::Fruit::impl::MemoryPool memory_pool;
  storage = std::unique_ptr<Poco::Fruit::impl::InjectorStorage>(new Poco::Fruit::impl::InjectorStorage(
      *(normalized_component.storage.storage), std::move(component.storage), memory_pool));

  using NormalizedComp =
      Poco::Fruit::impl::meta::ConstructComponentImpl(Poco::Fruit::impl::meta::Type<NormalizedComponentParams>...);
  using Comp1 = Poco::Fruit::impl::meta::ConstructComponentImpl(Poco::Fruit::impl::meta::Type<ComponentParams>...);
  // We don't check whether the construction of NormalizedComp or Comp resulted in errors here; if they did, the
  // instantiation
  // of NormalizedComponent<NormalizedComponentParams...> or Component<ComponentParams...> would have resulted in an
  // error already.

  using E = typename Poco::Fruit::impl::meta::InjectorImplHelper<P...>::template CheckConstructionFromNormalizedComponent<
      NormalizedComp, Comp1>::type;
  (void)typename Poco::Fruit::impl::meta::CheckIfError<E>::type();
}

template <typename... P>
template <typename T>
inline Poco::Fruit::impl::RemoveAnnotations<T> Injector<P...>::get() {
  using E = typename Poco::Fruit::impl::meta::InjectorImplHelper<P...>::template CheckGet<T>::type;
  (void)typename Poco::Fruit::impl::meta::CheckIfError<E>::type();
  return storage->template get<T>();
}

template <typename... P>
template <typename T>
inline Injector<P...>::operator T() {
  return get<T>();
}

template <typename... P>
template <typename AnnotatedC>
inline const std::vector<Poco::Fruit::impl::RemoveAnnotations<AnnotatedC>*>& Injector<P...>::getMultibindings() {

  using Op = Poco::Fruit::impl::meta::Eval<Poco::Fruit::impl::meta::CheckNormalizedTypes(
      Poco::Fruit::impl::meta::Vector<Poco::Fruit::impl::meta::Type<AnnotatedC>>)>;
  (void)typename Poco::Fruit::impl::meta::CheckIfError<Op>::type();

  return storage->template getMultibindings<AnnotatedC>();
}

template <typename... P>
FRUIT_DEPRECATED_DEFINITION(inline void Injector<P...>::eagerlyInjectAll()) {
  // Eagerly inject normal bindings.
  void* unused[] = {reinterpret_cast<void*>(
      storage->template get<Poco::Fruit::impl::meta::UnwrapType<
          Poco::Fruit::impl::meta::Eval<Poco::Fruit::impl::meta::AddPointerInAnnotatedType(Poco::Fruit::impl::meta::Type<P>)>>>())...};
  (void)unused;

  storage->eagerlyInjectMultibindings();
}

} // namespace Fruit
} // namespace Poco

#endif // FRUIT_INJECTOR_DEFN_H
