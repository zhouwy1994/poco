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

#ifndef FRUIT_COMPONENT_H
#define FRUIT_COMPONENT_H

// This include is not required here, but having it here shortens the include trace in error messages.
#include <Poco/Fruit/impl/injection_errors.h>

#include <Poco/Fruit/fruit_forward_decls.h>
#include <Poco/Fruit/impl/bindings.h>
#include <Poco/Fruit/impl/component_functors.defn.h>
#include <Poco/Fruit/impl/component_storage/component_storage.h>
#include <Poco/Fruit/impl/component_storage/partial_component_storage.h>
#include <Poco/Fruit/impl/meta/component.h>

namespace Poco{
namespace Fruit {

/**
 * A component (aka module) represents a collection of bindings.
 * You can think of a Component object as a UML component.
 *
 * The parameters can be of the form <P...> or <Required<R...>, P...> where:
 * * R... are the required types (types required to inject some types in P... but that are not provided by this
 *   Component), if any
 * * P... are the types provided by this Component.
 * No type can appear twice, not even once in R and once in P.
 *
 * See PartialComponent below for how to construct a Component.
 */
template <typename... Params>
class Component {
public:
  Component(Component&&) noexcept = default;

  Component& operator=(Component&&) = delete;
  Component& operator=(const Component&) = delete;

  /**
   * Converts a PartialComponent to an arbitrary Component, auto-injecting the missing types (if
   * any).
   * This is usually called implicitly when returning a component from a function. See PartialComponent for an example.
   */
  template <typename... Bindings>
  Component(PartialComponent<Bindings...>&& component) noexcept; // NOLINT(google-explicit-constructor)

private:
  // Do not use. Use Poco::Fruit::createComponent() instead.
  Component() = default;

  template <typename... Types>
  friend class Component;

  template <typename... Bindings>
  friend class PartialComponent;

  template <typename... OtherParams>
  friend class NormalizedComponent;

  template <typename... OtherParams>
  friend class Injector;

  template <typename... Bindings>
  friend class Poco::Fruit::impl::PartialComponentStorage;

  template <typename Component, typename... Args>
  friend class Poco::Fruit::impl::LazyComponentImpl;

  friend struct Poco::Fruit::impl::ComponentStorageEntry::LazyComponentWithNoArgs;

  template <typename Component, typename... Args>
  friend class Poco::Fruit::impl::ComponentInterfaceImpl;

  Poco::Fruit::impl::ComponentStorage storage;

  using Comp = Poco::Fruit::impl::meta::Eval<Poco::Fruit::impl::meta::ConstructComponentImpl(Poco::Fruit::impl::meta::Type<Params>...)>;

  using Check1 = typename Poco::Fruit::impl::meta::CheckIfError<Comp>::type;
  // Force instantiation of Check1.
  static_assert(true || sizeof(Check1), "");
};

/**
 * Constructs an empty component.
 *
 * Example usage:
 *
 * Poco::Fruit::Component<Foo> getFooComponent() {
 *   return Poco::Fruit::createComponent()
 *      .install(getComponent1)
 *      .install(getComponent2)
 *      .bind<Foo, FooImpl>();
 * }
 *
 * Since types are auto-injected when needed, just converting this to the desired component can suffice in some cases,
 * e.g.:
 *
 * Poco::Fruit::Component<Foo> getFooComponent() {
 *   return Poco::Fruit::createComponent();
 * }
 *
 * That works if Foo has an Inject typedef or a constructor wrapped in INJECT.
 */
PartialComponent<> createComponent();

/**
 * A partially constructed component.
 *
 * Client code should never write `PartialComponent'; always start the construction of a component with
 * Poco::Fruit::createComponent(), and end it by casting the PartialComponent to the desired Component (often done implicitly
 * by returning a PartialComponent from a function that has Component<...> as the return type).
 *
 * The template parameter is used to propagate information about bound types, it is purely an implementation detail;
 * users of the Fruit library can pretend that this class is not templated, in no case a specific template parameter is
 * required. All methods of this class return a PartialComponent, which allows to chain method invocations without
 * declaring a variable of type PartialComponent.
 *
 * Example usage:
 *
 * Poco::Fruit::Component<Foo> getFooComponent() {
 *   return Poco::Fruit::createComponent()
 *      .install(getComponent1)
 *      .install(getComponent2)
 *      .bind<Foo, FooImpl>();
 * }
 *
 * Note that no variable of type PartialComponent has been declared; this class should only be used for temporary
 * values.
 */
template <typename... Bindings>
class PartialComponent {
public:
  PartialComponent& operator=(PartialComponent&&) = delete;
  PartialComponent& operator=(const PartialComponent&) = delete;

  /**
   * This tells Fruit that "the implementation of I is C".
   * I must be a base class of C, and it's typically (but not necessarily) an abstract class.
   * C is typically a concrete class, but it doesn't have to be: for example, if A inherits from B and B inherits from C
   * you can specify bind<C, B>() and bind<B, A>().
   *
   * The most common use of this is to bind the type I to the type C, for example:
   *
   * class MyInterface {
   * public:
   *   virtual void foo() = 0;
   * };
   *
   * class MyImplementation {
   * public:
   *   INJECT(MyImplementation()) {}
   *
   *   void foo() {
   *     ...
   *   }
   * };
   *
   * Poco::Fruit::Component<MyInterface> getMyInterfaceComponent() {
   *   return Poco::Fruit::createComponent()
   *      .bind<MyInterface, MyImplementation>();
   * }
   *
   * The implementation class can be bound in any way, it doesn't need to be bound using constructor injection as above
   * (although that's a very common use case).
   *
   * You can bind an interface to a type bound using a constant binding (see the bindInstance method that takes a const&
   * for more details), however the interface will then also be considered bound with a constant binding, and you must
   * declare that in the returned Component's type. For example:
   *
   * Poco::Fruit::Component<const MyInterface> getMyInterfaceComponent() {
   *   static const MyImplementation my_implementation = MyImplementation();
   *   return Poco::Fruit::createComponent()
   *      .bindInstance(my_implementation)
   *      .bind<MyInterface, MyImplementation>();
   * }
   *
   * In addition to binding the type I to the type C, a `bind()` can also be used to bind a
   * std::function<std::unique_ptr<I>(Args...)> to a std::function<std::unique_ptr<C>(Args...)> or a
   * std::function<C(Args...)>. For example:
   *
   * Poco::Fruit::Component<std::function<std::unique_ptr<MyInterface>(int)>> getIFactoryComponent() {
   *   static const std::function<MyImplementation(int)> cFactory = [](int n) { return MyImplementation(n); };
   *   return Poco::Fruit::createComponent()
   *       .bind<MyInterface, MyImplementation>()
   *       .bindInstance(cFactory);
   * }
   *
   * Or alternatively you can do the same using constructor injection:
   *
   * class MyImplementation {
   * public:
   *   INJECT(MyImplementation(ASSISTED(int) n))
   *     : n(n) {
   *   }
   *   ...
   * };
   *
   * Poco::Fruit::Component<std::function<std::unique_ptr<MyInterface>(int)>> getIFactoryComponent() {
   *   return Poco::Fruit::createComponent()
   *       .bind<MyInterface, MyImplementation>();
   * }
   *
   * Fruit determines the actual binding(s) to generate based on the types you declare as provided in the returned
   * Component<> type (e.g. in the last example std::function<std::unique_ptr<MyInterface>(int)> is declared as provided
   * so Fruit will generate a factory binding instead of a normal MyInterface->MyImplementation binding.
   *
   * Fruit can also detect types that are needed for constructor/provider/factory bindings, and it will then use that
   * information to determine the desired binding. For example:
   *
   * class MyImplementation {
   * public:
   *   INJECT(MyImplementation(ASSISTED(int) n))
   *     : n(n) {
   *   }
   *   ...
   * };
   *
   * class Foo {
   * private:
   *   std::function<std::unique_ptr<MyInterface>(int)> factory;
   * public:
   *   INJECT(Foo(std::function<std::unique_ptr<MyInterface>(int)> factory))
   *     : factory(factory) {
   *   }
   * };
   *
   * Poco::Fruit::Component<Foo> getIFactoryComponent() {
   *   return Poco::Fruit::createComponent()
   *       // We want to bind Foo, which requires std::function<std::unique_ptr<MyInterface>(int)>.
   *       // So std::function<std::unique_ptr<MyInterface>(int)> will be bound to
   *       // std::function<std::unique_ptr<MyImplementation>(int)>, and that will be bound using constructor injection.
   *       .bind<MyInterface, MyImplementation>();
   * }
   *
   * All these cases support annotated injection, just wrap I and/or C in Poco::Fruit::Annotated<> if desired. For example:
   *
   * struct MyAnnotation{};
   *
   * Poco::Fruit::Component<Poco::Fruit::Annotated<MyAnnotation, MyInterface>> getMyInterfaceComponent() {
   *   return Poco::Fruit::createComponent()
   *      .bind<Poco::Fruit::Annotated<MyAnnotation, MyInterface>, MyImplementation>();
   * }
   */
  template <typename I, typename C>
  PartialComponent<Poco::Fruit::impl::Bind<I, C>, Bindings...> bind();

  /**
   * Registers Signature as the constructor signature to use to inject a type.
   *
   * Example usage:
   *
   * Poco::Fruit::createComponent()
   *     .registerConstructor<Foo(Bar*,Baz*)>() // Registers the constructor Foo::Foo(Bar*,Baz*)
   *
   * It's usually more convenient to use an INJECT macro or Inject typedef instead, e.g.:
   *
   * class Foo {
   * public:
   *   // This also declares the constructor
   *   INJECT(Foo(Bar* bar, Baz* baz));
   * ...
   * };
   *
   * or (equivalent):
   *
   * class Foo {
   * public:
   *   using Inject = Foo(Bar*, Baz*);
   *   Foo(Bar* bar, Baz* baz);
   * ...
   * };
   *
   * Use registerConstructor() when you want to inject the class C in different ways in different components (just make
   * sure those don't end up in the same injector, or use annotated injection to prevent the bindings from clashing),
   * or when C is a third-party class that can't be modified.
   *
   * This supports annotated injection, just wrap the desired types (return type and/or argument types of the signature)
   * with Poco::Fruit::Annotated<> if desired. For example:
   *
   * struct Annotation1 {};
   * struct Annotation2 {};
   *
   * struct Foo {
   *   Foo(Bar* bar) {...}
   * };
   *
   * Poco::Fruit::Component<Poco::Fruit::Annotated<Annotation1, Bar>> getBarComponent() {...}
   *
   * Poco::Fruit::Component<Poco::Fruit::Annotated<Annotation2, Foo>> getFooComponent() {
   *   return Poco::Fruit::createComponent()
   *       .install(getBarComponent)
   *       .registerConstructor<Poco::Fruit::Annotated<Annotation2, Foo>(Poco::Fruit::Annotated<Annotation1, Bar*>)>();
   * }
   *
   * This does *not* support assisted injection, for that you should use registerFactory() instead.
   *
   * The allowed argument types in the signature are, for any class (or fundamental) type C:
   *
   * C
   * C*
   * C&
   * const C*
   * const C&
   * shared_ptr<C>
   * Provider<C>
   * Provider<const C>
   * Annotated<Annotation, C>                   (for any type `Annotation')
   * Annotated<Annotation, C*>                  (for any type `Annotation')
   * Annotated<Annotation, C&>                  (for any type `Annotation')
   * Annotated<Annotation, const C*>            (for any type `Annotation')
   * Annotated<Annotation, const C&>            (for any type `Annotation')
   * Annotated<Annotation, shared_ptr<C>>       (for any type `Annotation')
   * Annotated<Annotation, Provider<C>>         (for any type `Annotation')
   * Annotated<Annotation, Provider<const C>>   (for any type `Annotation')
   */
  template <typename Signature>
  PartialComponent<Poco::Fruit::impl::RegisterConstructor<Signature>, Bindings...> registerConstructor();

  /**
   * Use this method to bind the type C to a specific instance.
   * The caller must ensure that the provided reference is valid for the entire lifetime of the component and of any
   * components or injectors that install this component; the caller must also ensure that the object is destroyed after
   * the last components/injectors using it are destroyed.
   *
   * Example usage:
   *
   * Component<Request> getRequestComponent(Request* request) {
   *   return Poco::Fruit::createComponent()
   *       .bindInstance(*request);
   * }
   *
   * NormalizedComponent<...> normalizedComponent = ...;
   * Request request;
   * Injector<...> injector(normalizedComponent,
   *                        getRequestComponent,
   *                        request));
   *
   * This should be used sparingly (you should let Fruit handle the object lifetime when possible), but in some cases it
   * is necessary; for example, if a web server creates an injector to handle each request, this method can be used to
   * inject the request itself as in the example above (see the Server page in the Fruit tutorial for more details).
   *
   * It's also possible to bind constants, see the documentation of the bindInstance() method taking a const& for
   * details.
   */
  template <typename C>
  PartialComponent<Poco::Fruit::impl::BindInstance<C, C>, Bindings...> bindInstance(C& instance);

  /**
   * Similar to the previous, but binds a const&. Note that the reference must still outlive the component/injector
   * as in the non-const case.
   * When using this method, you must declare that the type is constant in the Component type. For example:
   *
   * Component<const MyExpensiveClass> getMyExpensiveClassComponent() {
   *   static const MyExpensiveClass my_expensive_class = createMyExpensiveClass();
   *   return Poco::Fruit::createComponent()
   *       .bindInstance(my_expensive_class);
   * }
   *
   * Constant bindings can be used as other bindings, except that you can only inject the constant type (e.g. as a
   * constructor parameter) as:
   *
   * C
   * const C*
   * const C&
   * Provider<const C>
   * Annotated<Annotation, C>                   (for any type `Annotation')
   * Annotated<Annotation, const C*>            (for any type `Annotation')
   * Annotated<Annotation, const C&>            (for any type `Annotation')
   * Annotated<Annotation, Provider<const C>>   (for any type `Annotation')
   *
   * While you can't inject it as:
   *
   * C*
   * C&
   * shared_ptr<C>
   * Provider<C>
   * Annotated<Annotation, C*>                  (for any type `Annotation')
   * Annotated<Annotation, C&>                  (for any type `Annotation')
   * Annotated<Annotation, shared_ptr<C>>       (for any type `Annotation')
   * Annotated<Annotation, Provider<C>>         (for any type `Annotation')
   */
  template <typename C>
  PartialComponent<Poco::Fruit::impl::BindConstInstance<C, C>, Bindings...> bindInstance(const C& instance);

  /**
   * This is deleted to catch cases where the instance would likely be destroyed before the component/injectors.
   */
  template <typename C>
  PartialComponent<Poco::Fruit::impl::BindConstInstance<C, C>, Bindings...> bindInstance(C&&) = delete;

  /**
   * Similar to the first version of bindInstance(), but allows to specify an annotated type that
   * will be bound to the specified value.
   * For example, to bind an instance to the type Poco::Fruit::Annotated<Hostname, std::string>, you can use:
   *
   * Poco::Fruit::Component<Poco::Fruit::Annotated<Hostname, std::string>> getHostnameComponent(std::string* hostname) {
   *   Poco::Fruit::createComponent()
   *       .bindInstance<Poco::Fruit::Annotated<Hostname, std::string>>(*hostname);
   * }
   */
  template <typename AnnotatedType, typename C>
  PartialComponent<Poco::Fruit::impl::BindInstance<AnnotatedType, C>, Bindings...> bindInstance(C& instance);

  /**
   * Similar to the previous, but binds a const&. Example usage:
   *
   * Poco::Fruit::Component<Poco::Fruit::Annotated<Hostname, const std::string>> getHostnameComponent() {
   *   static const std::string hostname = determineHostname();
   *   Poco::Fruit::createComponent()
   *       .bindInstance<Poco::Fruit::Annotated<Hostname, std::string>>(hostname);
   * }
   *
   * See the documentation for the bindInstance() overload that takes a non-annotated const& for more details.
   */
  template <typename AnnotatedType, typename C>
  PartialComponent<Poco::Fruit::impl::BindConstInstance<AnnotatedType, C>, Bindings...> bindInstance(const C& instance);

  /**
   * This is deleted to catch cases where the instance would likely be destroyed before the component/injectors.
   */
  template <typename AnnotatedType, typename C>
  PartialComponent<Poco::Fruit::impl::BindConstInstance<AnnotatedType, C>, Bindings...> bindInstance(C&& instance);

  /**
   * Registers `provider' as a provider of C, where provider is a lambda with no captures returning either C or C*
   * (prefer returning a C by value instead of allocating a C using `new C', to avoid the allocation).
   *
   * When injecting a C, the arguments of the provider will be injected and the provider will then be called to create
   * the C instance, that will then be stored in the injector.
   *
   * If `provider' returns a pointer, it must be non-null; otherwise the program will abort.
   *
   * Example:
   *
   * Poco::Fruit::Component<Foo> getFooComponent() {
   *   return Poco::Fruit::createComponent()
   *       .install(getBarComponent)
   *       .install(getBazComponent)
   *       .registerProvider([](Bar* bar, Baz* baz) {
   *          Foo foo(bar, baz);
   *          foo.initialize();
   *          return foo;
   *       });
   * }
   *
   * As in the previous example, it's not necessary to specify the type parameter, it will be inferred by the compiler.
   *
   * registerProvider() can't be called with a plain function, but you can write a lambda that wraps the function to
   * achieve the same result.
   *
   * Registering stateful functors (including lambdas with captures) is NOT supported.
   * However, you can write something like:
   *
   * struct Functor {
   *   Functor(int n) {...}
   *   MyClass operator()(Foo* foo) const {...}
   * };
   *
   * Component<MyClass> getMyClassComponent() {
   *   static const Functor aFunctor(42);
   *   return Poco::Fruit::createComponent()
   *       .install(getFooComponent)
   *       .bindInstance(aFunctor)
   *       .registerProvider([](const Functor& functor, Foo* foo) { return functor(foo); });
   * }
   */
  template <typename Lambda>
  PartialComponent<Poco::Fruit::impl::RegisterProvider<Lambda>, Bindings...> registerProvider(Lambda lambda);

  /**
   * Similar to the previous version of registerProvider(), but allows to specify an annotated type
   * for the provider. This allows to inject annotated types in the parameters and/or bind the
   * provider to an annotated type. For example:
   *
   * struct MyAnnotation1 {};
   * struct MyAnnotation2 {};
   *
   * Component<Poco::Fruit::Annotated<Annotation1, Bar>> getBarComponent() {...}
   * Component<Baz> getBazComponent() {...}
   *
   * Poco::Fruit::Component<Poco::Fruit::Annotated<Annotation2, Foo>> getFooComponent() {
   *   return Poco::Fruit::createComponent()
   *       .install(getBarComponent)
   *       .install(getBazComponent)
   *       .registerProvider<
   *           Poco::Fruit::Annotated<Annotation2, Foo>(
   *               Poco::Fruit::Annotated<Annotation1, Bar*>,
   *               Baz*)
   *           >([](Bar* bar, Baz* baz) {
   *              Foo foo(bar, baz);
   *              foo.initialize();
   *              return foo;
   *           });
   * }
   */
  template <typename AnnotatedSignature, typename Lambda>
  PartialComponent<Poco::Fruit::impl::RegisterProvider<AnnotatedSignature, Lambda>, Bindings...>
  registerProvider(Lambda lambda);

  /**
   * Similar to bind<I, C>(), but adds a multibinding instead.
   *
   * Multibindings are independent from bindings; creating a binding with bind doesn't count as a multibinding, and
   * adding a multibinding doesn't allow to inject the type (it only allows to retrieve multibindings through the
   * getMultibindings method of the injector).
   *
   * Unlike bindings, where adding a the same binding twice is allowed (and ignored), adding the same multibinding
   * multiple times will result in the creation of multiple "equivalent" instances, that will all be returned by
   * getMultibindings().
   *
   * Another difference compared with normal bindings is that this can't be used to bind  a
   * std::function<std::unique_ptr<I>(Args...)> to a std::function<std::unique_ptr<C>(Args...)> or a
   * std::function<C(Args...)>.
   *
   * As bind(), this supports annotated injection, just wrap I and/or C in Poco::Fruit::Annotated<> if desired. See the
   * documentation of bind() for more details.
   */
  template <typename I, typename C>
  PartialComponent<Poco::Fruit::impl::AddMultibinding<I, C>, Bindings...> addMultibinding();

  /**
   * Similar to bindInstance(), but adds a multibinding instead.
   *
   * Multibindings are independent from bindings; creating a binding with bindInstance doesn't count as a
   * multibinding, and adding a multibinding doesn't allow to inject the type (it only allows to retrieve
   * multibindings through the getMultibindings method of the injector).
   *
   * Unlike bindings, where adding a the same binding twice is allowed (and ignored), adding several multibindings for
   * the same instance will result in duplicated values in the result of getMultibindings.
   *
   * Another difference compared to bindInstance() is that you can't use this to bind a const& (note that there is no
   * overload of this method that takes a const&).
   *
   * This method adds a multibinding for C. If the object implements an interface I and you want to add a multibinding
   * for that interface instead, you must cast the object to I& before passing it to this method.
   *
   * Note that this takes the instance by reference, not by value; it must remain valid for the entire lifetime of this
   * component and of any injectors created from this component.
   *
   * Example use:
   *
   * class MyClass {
   *   ...
   * };
   *
   * Poco::Fruit::Component<> getMyComponent() {
   *   static MyClass x = MyClass(...);
   *   static MyClass y = MyClass(...);
   *   return Poco::Fruit::createComponent()
   *       .addInstanceMultibinding(x)
   *       .addInstanceMultibinding(y);
   * }
   *
   * Poco::Fruit::Injector<> injector(getMyComponent);
   * // This vector contains {&x, &y}.
   * const std::vector<MyClass*>& objects = injector.getMultibindings<MyClass>();
   */
  template <typename C>
  PartialComponent<Poco::Fruit::impl::AddInstanceMultibinding<C>, Bindings...> addInstanceMultibinding(C& instance);

  /**
   * Similar to the previous version of addInstanceMultibinding(), but allows to specify an
   * annotated type.
   * Example use:
   *
   * struct MyAnnotation {};
   *
   * class MyClass {
   *   ...
   * };
   *
   * Poco::Fruit::Component<> getMyComponent() {
   *   static MyClass x = MyClass(...);
   *   static MyClass y = MyClass(...);
   *   return Poco::Fruit::createComponent()
   *       .addInstanceMultibinding<Poco::Fruit::Annotated<MyAnnotation, MyClass>>(x)
   *       .addInstanceMultibinding<Poco::Fruit::Annotated<MyAnnotation, MyClass>>(y);
   * }
   *
   * Poco::Fruit::Injector<> injector(getMyComponent);
   * // This vector contains {&x, &y}.
   * const std::vector<MyClass*>& objects = injector.getMultibindings<Poco::Fruit::Annotated<MyAnnotation, MyClass>>();
   */
  template <typename AnnotatedC, typename C>
  PartialComponent<Poco::Fruit::impl::AddInstanceMultibinding<AnnotatedC>, Bindings...> addInstanceMultibinding(C& instance);

  /**
   * Equivalent to calling addInstanceMultibinding() for each elements of `instances'.
   * See the documentation of addInstanceMultibinding() for more details.
   *
   * Note that this takes the vector by reference, not by value; the vector (and its elements) must remain valid for the
   * entire lifetime of this component and of any injectors created from this component.
   *
   * Example use:
   *
   * class MyClass {
   *   ...
   * };
   *
   * Poco::Fruit::Component<> getMyComponent() {
   *   static MyClass x = MyClass(...);
   *   static std::vector<MyClass> other_objects{MyClass(...), MyClass(...)};
   *   return Poco::Fruit::createComponent()
   *       .addInstanceMultibinding(x)
   *       .addInstanceMultibindings(other_objects);
   * }
   *
   * Poco::Fruit::Injector<> injector(getMyComponent);
   * // This vector contains {&x, &(other_objects[0]), &(other_objects[1])}.
   * const std::vector<MyClass*>& objects = injector.getMultibindings<MyClass>();
   */
  template <typename C>
  PartialComponent<Poco::Fruit::impl::AddInstanceVectorMultibindings<C>, Bindings...>
  addInstanceMultibindings(std::vector<C>& instances);

  /**
   * Similar to the previous version of addInstanceMultibindings(), but it allows to specify an annotated type.
   *
   * Example use:
   *
   * class MyClass {
   *   ...
   * };
   *
   * Poco::Fruit::Component<> getMyComponent() {
   *   static MyClass x = MyClass(...);
   *   static std::vector<MyClass> other_objects{MyClass(...), MyClass(...)};
   *   return Poco::Fruit::createComponent()
   *       .addInstanceMultibinding<Poco::Fruit::Annotated<MyAnnotation, MyClass>>(x)
   *       .addInstanceMultibindings<Poco::Fruit::Annotated<MyAnnotation, MyClass>>(other_objects);
   * }
   *
   * Poco::Fruit::Injector<> injector(getMyComponent);
   * // This vector contains {&x, &(other_objects[0]), &(other_objects[1])}.
   * const std::vector<MyClass*>& objects = injector.getMultibindings<Poco::Fruit::Annotated<MyAnnotation, MyClass>>();
   */
  template <typename AnnotatedC, typename C>
  PartialComponent<Poco::Fruit::impl::AddInstanceVectorMultibindings<AnnotatedC>, Bindings...>
  addInstanceMultibindings(std::vector<C>& instances);

  /**
   * Similar to registerProvider, but adds a multibinding instead.
   *
   * Multibindings are independent from bindings; creating a binding with registerProvider doesn't count as a
   * multibinding, and adding a multibinding doesn't allow to inject the type (it only allows to retrieve multibindings
   * through the getMultibindings method of the injector).
   *
   * Unlike bindings, where adding a the same binding twice is allowed (and ignored), adding the same multibinding
   * provider multiple times will result in the creation of multiple "equivalent" instances, that will all be returned
   * by getMultibindings.
   * It is good practice to add the multibindings in a component that is "close" to the injector in the get*Component
   * call chain, to avoid adding the same multibinding more than once.
   *
   * Example use:
   *
   * class MyClass {
   * public:
   *   MyClass(int n) {...}
   * };
   *
   * Poco::Fruit::Component<> getMyComponent() {
   *   return Poco::Fruit::createComponent()
   *       .addMultibindingProvider([]() { return MyClass(10); })
   *       .addMultibindingProvider([]() { return MyClass(10); })
   *       .addMultibindingProvider([]() { return MyClass(20); });
   * }
   *
   * Poco::Fruit::Injector<> injector(getMyComponent);
   * // This vector contains {&x, &y, &z} where x and y are MyClass objects constructed with 10 and z is a MyClass
   * // object constructed with 20.
   * const std::vector<MyClass*>& objects = injector.getMultibindings<MyClass>();
   *
   * Note that this method adds a multibinding for the type returned by the provider. If the returned object implements
   * an interface I and you want to add a multibinding for that interface instead, you should cast the pointer to I*
   * before returning it.
   */
  template <typename Lambda>
  PartialComponent<Poco::Fruit::impl::AddMultibindingProvider<Lambda>, Bindings...> addMultibindingProvider(Lambda lambda);

  /**
   * Similar to the previous version of addMultibindingProvider(), but allows to specify an annotated type
   * for the provider. This allows to inject annotated types in the parameters and/or bind the
   * provider to an annotated type.
   *
   * Example use:
   *
   * struct MyAnnotation1 {};
   * struct MyAnnotation2 {};
   *
   * Component<Poco::Fruit::Annotated<Annotation1, Bar>> getBarComponent() {...}
   * Component<Baz> getBazComponent() {...}
   *
   * Poco::Fruit::Component<> getFooComponent() {
   *   return Poco::Fruit::createComponent()
   *       .install(getBarComponent)
   *       .install(getBazComponent)
   *       .registerMultibindingProvider<
   *           Poco::Fruit::Annotated<Annotation2, Foo>(
   *               Poco::Fruit::Annotated<Annotation1, Bar*>,
   *               Baz*)
   *           >([](Bar* bar, Baz* baz) {
   *              Foo foo(bar, baz);
   *              foo.initialize();
   *              return foo;
   *           });
   * }
   *
   *
   * Poco::Fruit::Injector<> injector(getFooComponent);
   * // This vector contains {&x} where x is an instance of Foo constructed using the lambda above, with injected
   * // instances of Bar and Baz.
   * const std::vector<MyClass*>& objects = injector.getMultibindings<Poco::Fruit::Annotated<Annotation2, Foo>>();
   */
  template <typename AnnotatedSignature, typename Lambda>
  PartialComponent<Poco::Fruit::impl::AddMultibindingProvider<AnnotatedSignature, Lambda>, Bindings...>
  addMultibindingProvider(Lambda lambda);

  /**
   * Registers `factory' as a factory of C, where `factory' is a lambda with no captures returning C.
   * This is typically used for assisted injection (but it can also be used if no parameters are assisted).
   *
   * C can be any class (or fundamental) type. If C is std::unique_ptr<T>, the factory together with a bind<I,C> in the
   * same component will automatically bind the corresponding std::function that returns a std::unique_ptr<I>.
   * See the documentation of bind() for more details.
   *
   * The returned type can't be a pointer type. If you don't want to return it by value, you should return a
   * std::unique_ptr instead.
   *
   * Example:
   *
   * Component<std::function<std::unique_ptr<MyClass>(int)>> getMyClassComponent() {
   *   Poco::Fruit::createComponent()
   *       .install(getFooComponent)
   *       .registerFactory<std::unique_ptr<MyClass>(Foo*, Poco::Fruit::Assisted<int>)>(
   *          [](Foo* foo, int n) {
   *              return std::unique_ptr<MyClass>(new MyClass(foo, n));
   *          });
   * }
   *
   * Injector<std::function<std::unique_ptr<MyClass>(int)>> injector(getMyClassComponent);
   *
   * std::function<std::unique_ptr<MyClass>(int)> factory(injector);
   * std::unique_ptr<MyClass> x = factory(42);
   *
   * The parameters marked as Assisted will become parameters of the std::function (in the same order), while the others
   * (e.g. Foo in the example above) will be injected.
   *
   * Unlike registerProvider(), where the signature is inferred, for this method the signature (including any Assisted
   * annotations) must be specified explicitly, while the second template parameter is inferred.
   *
   * If the only thing that the factory does is to call new and the constructor of the class, it's usually more
   * convenient to use an Inject typedef or INJECT macro instead, e.g. the following are equivalent to the above:
   *
   * class MyClass {
   * public:
   *    using Inject = MyClass(Foo*, Assisted<int>);
   *
   *    MyClass(Foo* foo, int n) {...}
   * };
   *
   * or:
   *
   * class MyClass {
   * public:
   *    INJECT(MyClass(Foo* foo, ASSISTED(int) n)) {...}
   * };
   *
   * Use registerFactory() when you want to inject the class in different ways in different components (just make sure
   * those don't end up in the same injector), or when MyClass is a third-party class that can't be modified.
   *
   * registerFactory() can't be called with a plain function, but you can write a lambda that wraps the function to
   * achieve the same result.
   *
   * Registering stateful functors (including lambdas with captures) is NOT supported.
   * However, you can write something like:
   *
   * struct Functor {
   *   Functor(float x) {...}
   *   std::unique_ptr<MyClass> operator()(Foo* foo, int n) {...}
   * };
   *
   * Component<std::function<std::unique_ptr<MyClass>(int)>> getMyClassComponent() {
   *   static const Functor aFunctor(42.0);
   *   return Poco::Fruit::createComponent()
   *       ... // Bind Foo
   *       .bindInstance(aFunctor)
   *       .registerFactory<
   *           std::unique_ptr<MyClass>(
   *               Functor functor,
   *               Foo*,
   *               Assisted<int>)
   *           >([](Functor functor, Foo* foo, int n) {
   *               return functor(foo, n);
   *           });
   * }
   */
  template <typename DecoratedSignature, typename Factory>
  PartialComponent<Poco::Fruit::impl::RegisterFactory<DecoratedSignature, Factory>, Bindings...>
  registerFactory(Factory factory);

  /**
   * Adds the bindings (and multibindings) in the Component obtained by calling fun(args...) to the current component.
   *
   * For example, these component functions:
   * Poco::Fruit::Component<Foo> getComponent1();
   * Poco::Fruit::Component<Bar> getComponent2(int n, std::string s);
   *
   * can be combined as:
   *
   * Poco::Fruit::Component<Foo, Bar> getFooBarComponent() {
   *   return Poco::Fruit::createComponent()
   *      .install(getComponent1)
   *      .install(getComponent2, 5, std::string("Hello"));
   * }
   *
   * If any `args` are provided, they must be:
   * - Copy-constructible
   * - Move-constructible
   * - Assignable
   * - Move-assignable
   * - Equality comparable (i.e., operator== must be defined for two values of that type)
   * - Hashable (i.e., std::hash must be defined for values of that type)
   *
   * Note that this only applies to `args`. E.g. in the example above `int` and `std::string` must satisfy this
   * requirement (and they do), but `Foo` and `Bar` don't need to.
   *
   * Args and FormalArgs (if any) must be the same types; or to be precise, each type in Args must be convertible into
   * the corresponding type in FormalArgs.
   *
   * A lambda with no captures can also be used as the first argument, for example:
   *
   * Poco::Fruit::Component<Foo, Bar> getFooBarComponent() {
   *   return Poco::Fruit::createComponent()
   *      .install([]() { return getComponent1(); })
   *      .install([](int n) { return getComponent2(n, std::string("Hello")); }, 5);
   * }
   *
   * These two install() calls are equivalent to the previous ones.
   *
   * As in the example, the template parameters for this method will be inferred by the compiler, it's not necessary to
   * specify them explicitly.
   *
   * Fruit automatically de-duplicates install() calls, so they're effectively memoized (within each injector).
   * For example, in this code:
   *
   * Poco::Fruit::Component<Foo> getFooComponent() {...}
   *
   * Poco::Fruit::Component<Bar> getBarComponent() {
   *   return Poco::Fruit::createComponent()
   *       .install(getFooComponent)
   *       .bind<Bar, BarImpl>();
   * }
   *
   * Poco::Fruit::Component<Baz> getBazComponent() {
   *   return Poco::Fruit::createComponent()
   *       .install(getFooComponent)
   *       .bind<Baz, BazImpl>();
   * }
   *
   * Poco::Fruit::Component<Bar, Baz> getBarBazComponent() {
   *   return Poco::Fruit::createComponent()
   *       .install(getBarComponent)
   *       .install(getBazComponent);
   * }
   *
   * Poco::Fruit::Injector<Bar, Baz> injector(getBarBazComponent);
   *
   *
   * getFooComponent() will only be called once.
   * For Component functions with arguments, only one call will be done for each set of arguments, but multiple calls
   * might be made if multiple sets of arguments are used.
   *
   * If you actually want a Component function to be called/installed multiple times (e.g. if it binds a multibinding
   * and you actually want multiple multibindings to be bound) you can add a dummy argument and specify different values
   * for that argument when installing the component.
   */
  template <typename... OtherComponentParams, typename... FormalArgs, typename... Args>
  PartialComponent<Poco::Fruit::impl::InstallComponent<Poco::Fruit::Component<OtherComponentParams...>(FormalArgs...)>, Bindings...>
  install(Poco::Fruit::Component<OtherComponentParams...> (*)(FormalArgs...), Args&&... args);

  /**
   * Similar to install(), but allows to install a variable number of component functions instead of just 1. This
   * additional flexibility is sometimes useful in templated `get*Component` functions and for other advanced use-cases.
   *
   * To use this method, wrap each get*Component function with its args in a Poco::Fruit::ComponentFunction<...> object (using
   * the helper function Poco::Fruit::componentFunction), then pass all the Poco::Fruit::ComponentFunction<...> objects (which can
   * potentially have different params) to this method.
   *
   * For example:
   *
   * Poco::Fruit::Component<Foo, Bar> getBarBazComponent() {
   *   return Poco::Fruit::createComponent()
   *       .installComponentFunctions(
   *           Poco::Fruit::componentFunction(getFooComponent, a, b, c),
   *           Poco::Fruit::componentFunction(getBarComponent, x, y));
   * }
   *
   * Is equivalent to:
   *
   * Poco::Fruit::Component<Foo, Bar> getBarBazComponent() {
   *   return Poco::Fruit::createComponent()
   *       .install(getFooComponent, a, b, c)
   *       .install(getBarComponent, x, y);
   * }
   * 
   * This is a simple example to show the idea, however in a simple case like this it's easier to just use install().
   */
  template <typename... ComponentFunctions>
  PartialComponent<Poco::Fruit::impl::InstallComponentFunctions<ComponentFunctions...>, Bindings...>
  installComponentFunctions(ComponentFunctions... componentFunctions);

  /**
   * This class is returned by PartialComponent::replace, see the documentation of that method for more information.
   */
  template <typename ReplacedComponent, typename... GetReplacedComponentFormalArgs>
  class PartialComponentWithReplacementInProgress {
  private:
    using storage_t = Poco::Fruit::impl::PartialComponentStorage<
        Poco::Fruit::impl::PartialReplaceComponent<ReplacedComponent(GetReplacedComponentFormalArgs...)>, Bindings...>;

  public:
    template <typename... FormalArgs, typename... Args>
    PartialComponent<Poco::Fruit::impl::ReplaceComponent<ReplacedComponent(GetReplacedComponentFormalArgs...),
                                                   ReplacedComponent(FormalArgs...)>,
                     Bindings...>
    with(ReplacedComponent (*)(FormalArgs...), Args&&... args);

    PartialComponentWithReplacementInProgress(storage_t storage) // NOLINT(google-explicit-constructor)
       : storage(storage) {}

  private:
    storage_t storage;

    PartialComponentWithReplacementInProgress() = delete;
  };

  /**
   * This allows to replace an installed Component with another one. This is useful for testing.
   * For example, if you have these components:
   *
   * Poco::Fruit::Component<MyDependency> getDependencyComponent() {...}
   *
   * Poco::Fruit::Component<Foo> getFooComponent() {
   *     return Poco::Fruit::createComponent()
   *         .install(getDependencyComponent)
   *         .bind<Foo, FooImpl>();
   * }
   *
   * Poco::Fruit::Component<Bar> getBarComponent() {
   *     return Poco::Fruit::createComponent()
   *         .install(getFooComponent)
   *         .bind<Bar, BarImpl>();
   * }
   *
   * When you test Bar, you might want to replace getDependencyComponent with a component that binds a fake
   * MyDependency:
   *
   * Poco::Fruit::Component<MyDependency> getFakeDependencyComponent() {...}
   *
   * To do so, you can define a component like:
   *
   * Poco::Fruit::Component<Bar> getBarComponentWithFakeDependency() {
   *     return Poco::Fruit::createComponent()
   *         .replace(getDependencyComponent).with(getFakeDependencyComponent)
   *         .install(getBarComponent);
   * }
   *
   * This component is equivalent to:
   *
   * Poco::Fruit::Component<Bar> getBarComponentWithFakeDependency() {
   *     return Poco::Fruit::createComponent()
   *         .install(getFakeDependencyComponent)
   *         .bind<Foo, FooImpl>()
   *         .bind<Bar, BarImpl>();
   * }
   *
   * However this way you don't need to duplicate the bindings for Foo and Bar, and you don't even need to include them
   * in the translation unit (i.e., cc/cpp file) that defines getBarComponentWithFakeDependency().
   * In codebases with many layers, this can save a lot of duplication.
   *
   * Note that the .replace(...).with(...) must appear *before* installing the component to which it's applied to;
   * e.g., in the example above note how we install getBarComponent after the replacement in
   * getBarComponentWithFakeDependency.
   * If you add a replacement after the replaced component has been installed, Fruit will report an error at run-time.
   *
   * In the example above, the replaced and replacement component functions had no arguments, however it's also possible
   * to replace component functions with args. The arguments of the replaced and replacement component functions are
   * independent; for example .replace(getDependencyComponentWithArgs, 15).with(myFakeComponentWithNoArgs) is allowed
   * and it would replace all install(getDependencyComponentWithArgs, 15) calls with install(myFakeComponentWithNoArgs).
   *
   * The component types returned by the replaced and replacement components must be the same. For example, this is NOT
   * allowed:
   *
   * Poco::Fruit::Component<MyDependency, SomethingElse> getFakeDependencyComponentWithSomethingElse() {...}
   *
   * Poco::Fruit::Component<Bar> getBarComponentWithFakeDependency() {
   *     return Poco::Fruit::createComponent()
   *         .replace(getDependencyComponent).with(getFakeDependencyComponentWithSomethingElse) // error!
   *         .install(getBarComponent);
   * }
   *
   * But replacing a replaced component is allowed:
   *
   * Poco::Fruit::Component<MyDependency> getOtherFakeDependencyComponent() {...}
   *
   * Poco::Fruit::Component<Bar> getBarComponentWithOtherFakeDependency() {
   *     return Poco::Fruit::createComponent()
   *         // The two replacements can appear in any order, but they must both be before the install().
   *         .replace(getFakeDependencyComponent).with(getOtherFakeDependencyComponent)
   *         .replace(getDependencyComponent).with(getFakeDependencyComponent)
   *         .install(getBarComponent);
   * }
   *
   * Of course this is a simple example, in the real world the replacements and the install would probably come from
   * other components.
   *
   * And note that you can also replace components that define replacements, for example:
   *
   * Poco::Fruit::Component<> getFakeDependencyReplacementComponent() {
   *     return Poco::Fruit::createComponent()
   *         .replace(getDependencyComponent).with(getFakeDependencyComponentWithSomethingElse);
   * }
   *
   * Poco::Fruit::Component<...> getComponent() {
   *     return Poco::Fruit::createComponent()
   *         .replace(getFakeDependencyReplacementComponent).with(...)
   *         .install(...);
   * }
   *
   * Replacements are only installed if the replaced component is installed, otherwise they are ignored.
   * In the first example above, if getFooComponent didn't install getDependencyComponent, when a test creates an
   * injector for getBarComponentWithFakeDependency it would not install getFakeDependencyComponent.
   */
  template <typename... OtherComponentParams, typename... FormalArgs, typename... Args>
  typename PartialComponent<Bindings...>::template PartialComponentWithReplacementInProgress<
      Poco::Fruit::Component<OtherComponentParams...>, FormalArgs...>
  replace(Poco::Fruit::Component<OtherComponentParams...> (*)(FormalArgs...), Args&&... args);

  ~PartialComponent() = default;

  // Do not use. Use Poco::Fruit::createComponent() instead.
  PartialComponent() = delete;

  // Do not use. Only use PartialComponent for temporaries, and then convert it to a Component.
  PartialComponent(const PartialComponent&) = delete;
  PartialComponent(PartialComponent&&) = delete;

private:
  template <typename... OtherBindings>
  friend class PartialComponent;

  template <typename... Types>
  friend class Component;

  Poco::Fruit::impl::PartialComponentStorage<Bindings...> storage;

  PartialComponent(Poco::Fruit::impl::PartialComponentStorage<Bindings...> storage); // NOLINT(google-explicit-constructor)

  template <typename NewBinding>
  using OpFor = typename Poco::Fruit::impl::meta::OpForComponent<Bindings...>::template AddBinding<NewBinding>;

  friend PartialComponent<> createComponent();
};

} // namespace Fruit
} // namespace Poco

#include <Poco/Fruit/impl/component.defn.h>

#endif // FRUIT_COMPONENT_H
