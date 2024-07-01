#!/usr/bin/env python3
#  Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from absl.testing import parameterized
from fruit_test_common import *

COMMON_DEFINITIONS = '''
    #include "test_common.h"

    struct X;
    struct Y;
    struct Z;

    struct Annotation1 {};
    using XAnnot1 = Fruit::Annotated<Annotation1, X>;
    using YAnnot1 = Fruit::Annotated<Annotation1, Y>;
    using ZAnnot1 = Fruit::Annotated<Annotation1, Z>;
    using ConstXAnnot1 = Fruit::Annotated<Annotation1, const X>;
    using ConstYAnnot1 = Fruit::Annotated<Annotation1, const Y>;
    using ConstZAnnot1 = Fruit::Annotated<Annotation1, const Z>;

    struct Annotation2 {};
    using XAnnot2 = Fruit::Annotated<Annotation2, X>;
    using YAnnot2 = Fruit::Annotated<Annotation2, Y>;
    using ZAnnot2 = Fruit::Annotated<Annotation2, Z>;
    using ConstXAnnot2 = Fruit::Annotated<Annotation2, const X>;
    using ConstYAnnot2 = Fruit::Annotated<Annotation2, const Y>;
    using ConstZAnnot2 = Fruit::Annotated<Annotation2, const Z>;

    struct Annotation3 {};
    '''

CONSTRUCTOR_BINDING = (
    '',
    '.registerConstructor<XAnnot()>()')
INTERFACE_BINDING = (
    '''
        struct Y : public X {};
    ''',
    '''
        .bind<XAnnot, YAnnot>()
        .registerConstructor<YAnnot()>()
    ''')
INTERFACE_BINDING2 = (
    '''
        struct Y2 : public X {};
    ''',
    '''
        .bind<XAnnot, Y2Annot>()
        .registerConstructor<Y2Annot()>()
    ''')
INSTALL = (
    '''
        Fruit::Component<XAnnot> getParentComponent() {
          return Fruit::createComponent()
            .registerConstructor<XAnnot()>();
        }
    ''',
    '.install(getParentComponent)')
INSTALL2 = (
    '''
        Fruit::Component<XAnnot> getParentComponent2() {
          return Fruit::createComponent()
            .registerConstructor<XAnnot()>();
        }
    ''',
    '.install(getParentComponent2)')
CONST_BINDING_FROM_INSTALL = (
    '''
        Fruit::Component<const XAnnot> getParentComponent() {
          return Fruit::createComponent()
            .registerConstructor<XAnnot()>();
        }
    ''',
    '.install(getParentComponent)')
CONST_BINDING_FROM_INSTALL2 = (
    '''
        Fruit::Component<const XAnnot> getParentComponent2() {
          return Fruit::createComponent()
            .registerConstructor<XAnnot()>();
        }
    ''',
    '.install(getParentComponent2)')
CONST_BINDING = (
    '''
        const X x{};
    ''',
    '.bindInstance<XAnnot, X>(x)')
CONST_BINDING2 = (
    '''
        const X x2{};
    ''',
    '.bindInstance<XAnnot, X>(x2)')

class TestBindingClash(parameterized.TestCase):
    @multiple_named_parameters([
        ('CONSTRUCTOR_BINDING + INSTALL',) + CONSTRUCTOR_BINDING + INSTALL,
        ('INTERFACE_BINDING + INSTALL',) + INTERFACE_BINDING + INSTALL,
        ('INSTALL + INSTALL2',) + INSTALL + INSTALL2,
        ('CONSTRUCTOR_BINDING + CONST_BINDING_FROM_INSTALL',) + CONSTRUCTOR_BINDING + CONST_BINDING_FROM_INSTALL,
        ('INTERFACE_BINDING + CONST_BINDING_FROM_INSTALL',) + INTERFACE_BINDING + CONST_BINDING_FROM_INSTALL,
        ('INSTALL2 + CONST_BINDING_FROM_INSTALL',) + INSTALL2 + CONST_BINDING_FROM_INSTALL,
        ('CONST_BINDING_FROM_INSTALL + INSTALL2',) + CONST_BINDING_FROM_INSTALL + INSTALL2,
        ('CONST_BINDING + INSTALL2',) + CONST_BINDING + INSTALL2,
        ('CONST_BINDING_FROM_INSTALL + CONST_BINDING_FROM_INSTALL2',) + CONST_BINDING_FROM_INSTALL + CONST_BINDING_FROM_INSTALL2,
        ('CONST_BINDING + CONST_BINDING_FROM_INSTALL',) + CONST_BINDING + CONST_BINDING_FROM_INSTALL,
    ], [
        ('No annotation', 'X', 'Y', 'Y2'),
        ('With annotation', 'Fruit::Annotated<Annotation1, X>', 'Fruit::Annotated<Annotation2, Y>', 'Fruit::Annotated<Annotation3, Y2>'),
    ])
    def test_clash_with_install(self,
            binding1_preparation, binding1, binding2_preparation, binding2, XAnnot, YAnnot, Y2Annot):
        source = '''
            struct X{};
    
            %s
            %s
    
            Fruit::Component<XAnnot> getComponent() {
              return Fruit::createComponent()
                  %s
                  %s;
            }
            ''' % (binding1_preparation, binding2_preparation, binding1, binding2)
        expect_compile_error(
            'DuplicateTypesInComponentError<XAnnot>',
            'The installed component provides some types that are already provided by the current component.',
            COMMON_DEFINITIONS,
            source,
            locals())

    @multiple_named_parameters([
        ('CONSTRUCTOR_BINDING + CONSTRUCTOR_BINDING',) + CONSTRUCTOR_BINDING + CONSTRUCTOR_BINDING,
        ('CONSTRUCTOR_BINDING + INTERFACE_BINDING',) + CONSTRUCTOR_BINDING + INTERFACE_BINDING,
        ('INTERFACE_BINDING + CONSTRUCTOR_BINDING',) + INTERFACE_BINDING + CONSTRUCTOR_BINDING,
        ('INTERFACE_BINDING + INTERFACE_BINDING2',) + INTERFACE_BINDING + INTERFACE_BINDING2,
        ('INSTALL + CONSTRUCTOR_BINDING',) + INSTALL + CONSTRUCTOR_BINDING,
        ('INSTALL + INTERFACE_BINDING',) + INSTALL + INTERFACE_BINDING,
        ('CONST_BINDING_FROM_INSTALL + CONSTRUCTOR_BINDING',) + CONST_BINDING_FROM_INSTALL + CONSTRUCTOR_BINDING,
        ('CONST_BINDING_FROM_INSTALL + INTERFACE_BINDING',) + CONST_BINDING_FROM_INSTALL + INTERFACE_BINDING,
        ('CONST_BINDING + CONSTRUCTOR_BINDING',) + CONST_BINDING + CONSTRUCTOR_BINDING,
        ('CONST_BINDING + INTERFACE_BINDING',) + CONST_BINDING + INTERFACE_BINDING,
        ('CONSTRUCTOR_BINDING + CONST_BINDING',) + CONSTRUCTOR_BINDING + CONST_BINDING,
        ('INTERFACE_BINDING + CONST_BINDING',) + INTERFACE_BINDING + CONST_BINDING,
        ('INSTALL2 + CONST_BINDING',) + INSTALL2 + CONST_BINDING,
        ('CONST_BINDING_FROM_INSTALL + CONST_BINDING',) + CONST_BINDING_FROM_INSTALL + CONST_BINDING,
        ('CONST_BINDING + CONST_BINDING2',) + CONST_BINDING + CONST_BINDING2,
    ], [
        ('No annotation', 'X', 'Y', 'Y2'),
        ('With annotation', 'Fruit::Annotated<Annotation1, X>', 'Fruit::Annotated<Annotation2, Y>', 'Fruit::Annotated<Annotation3, Y2>'),
    ])
    def test_clash_with_binding(self, binding1_preparation, binding1, binding2_preparation, binding2, XAnnot, YAnnot, Y2Annot):
        source = '''
            struct X{};
    
            %s
            %s
    
            Fruit::Component<XAnnot> getComponent() {
              return Fruit::createComponent()
                  %s
                  %s;
            }
    
            ''' % (binding1_preparation, binding2_preparation, binding1, binding2)
        expect_compile_error(
            'TypeAlreadyBoundError<XAnnot>',
            'Trying to bind C but it is already bound.',
            COMMON_DEFINITIONS,
            source,
            locals())

    CONSTRUCTOR_BINDING_ANNOT1 = (
        '',
        '.registerConstructor<XAnnot1()>()')
    CONSTRUCTOR_BINDING_ANNOT2 = (
        '',
        '.registerConstructor<XAnnot2()>()')
    INTERFACE_BINDING_ANNOT1 = (
        '''
            struct Y : public X {};
        ''',
        '''
            .bind<XAnnot1, YAnnot1>()
            .registerConstructor<YAnnot1()>()
        ''')
    INTERFACE_BINDING_ANNOT2 = (
        '''
            struct Z : public X {};
        ''',
        '''
            .bind<XAnnot2, ZAnnot2>()
            .registerConstructor<ZAnnot2()>()
        ''')
    INSTALL_ANNOT1 = (
        '''
            Fruit::Component<XAnnot1> getParentComponent1() {
              return Fruit::createComponent()
                .registerConstructor<XAnnot1()>();
            }
        ''',
        '.install(getParentComponent1)')
    INSTALL_ANNOT2 = (
        '''
            Fruit::Component<XAnnot2> getParentComponent2() {
              return Fruit::createComponent()
                .registerConstructor<XAnnot2()>();
            }
        ''',
        '.install(getParentComponent2)')
    CONST_BINDING_FROM_INSTALL_ANNOT1 = (
        '''
            Fruit::Component<ConstXAnnot1> getParentComponent1() {
              return Fruit::createComponent()
                .registerConstructor<XAnnot1()>();
            }
        ''',
        '.install(getParentComponent1)')
    CONST_BINDING_FROM_INSTALL_ANNOT2 = (
        '''
            Fruit::Component<ConstXAnnot2> getParentComponent2() {
              return Fruit::createComponent()
                .registerConstructor<XAnnot2()>();
            }
        ''',
        '.install(getParentComponent2)')
    CONST_BINDING_ANNOT1 = (
        '''
            const X x1{};
        ''',
        '.bindInstance<XAnnot1, X>(x1)')
    CONST_BINDING_ANNOT2 = (
        '''
            const X x2{};
        ''',
        '.bindInstance<XAnnot2, X>(x2)')

    @parameterized.named_parameters([
        ('CONSTRUCTOR_BINDING_ANNOT1 + CONSTRUCTOR_BINDING_ANNOT2',) + CONSTRUCTOR_BINDING_ANNOT1 + CONSTRUCTOR_BINDING_ANNOT2,
        ('CONSTRUCTOR_BINDING_ANNOT1 + INTERFACE_BINDING_ANNOT2',) + CONSTRUCTOR_BINDING_ANNOT1 + INTERFACE_BINDING_ANNOT2,
        ('INTERFACE_BINDING_ANNOT1 + CONSTRUCTOR_BINDING_ANNOT2',) + INTERFACE_BINDING_ANNOT1 + CONSTRUCTOR_BINDING_ANNOT2,
        ('INTERFACE_BINDING_ANNOT1 + INTERFACE_BINDING_ANNOT2',) + INTERFACE_BINDING_ANNOT1 + INTERFACE_BINDING_ANNOT2,
        ('INSTALL_ANNOT1 + CONSTRUCTOR_BINDING_ANNOT2',) + INSTALL_ANNOT1 + CONSTRUCTOR_BINDING_ANNOT2,
        ('INSTALL_ANNOT1 + INTERFACE_BINDING_ANNOT2',) + INSTALL_ANNOT1 + INTERFACE_BINDING_ANNOT2,
        ('CONST_BINDING_FROM_INSTALL_ANNOT1 + CONSTRUCTOR_BINDING_ANNOT2',) + CONST_BINDING_FROM_INSTALL_ANNOT1 + CONSTRUCTOR_BINDING_ANNOT2,
        ('CONST_BINDING_ANNOT1 + CONSTRUCTOR_BINDING_ANNOT2',) + CONST_BINDING_ANNOT1 + CONSTRUCTOR_BINDING_ANNOT2,
        ('CONST_BINDING_FROM_INSTALL_ANNOT1 + INTERFACE_BINDING_ANNOT2',) + CONST_BINDING_FROM_INSTALL_ANNOT1 + INTERFACE_BINDING_ANNOT2,
        ('CONST_BINDING_ANNOT1 + INTERFACE_BINDING_ANNOT2',) + CONST_BINDING_ANNOT1 + INTERFACE_BINDING_ANNOT2,
        ('CONSTRUCTOR_BINDING_ANNOT1 + INSTALL_ANNOT2',) + CONSTRUCTOR_BINDING_ANNOT1 + INSTALL_ANNOT2,
        ('INTERFACE_BINDING_ANNOT1 + INSTALL_ANNOT2',) + INTERFACE_BINDING_ANNOT1 + INSTALL_ANNOT2,
        ('CONSTRUCTOR_BINDING_ANNOT1 + CONST_BINDING_FROM_INSTALL_ANNOT2',) + CONSTRUCTOR_BINDING_ANNOT1 + CONST_BINDING_FROM_INSTALL_ANNOT2,
        ('CONSTRUCTOR_BINDING_ANNOT1 + CONST_BINDING_ANNOT2',) + CONSTRUCTOR_BINDING_ANNOT1 + CONST_BINDING_ANNOT2,
        ('INTERFACE_BINDING_ANNOT1 + CONST_BINDING_FROM_INSTALL_ANNOT2',) + INTERFACE_BINDING_ANNOT1 + CONST_BINDING_FROM_INSTALL_ANNOT2,
        ('INTERFACE_BINDING_ANNOT1 + CONST_BINDING_ANNOT2',) + INTERFACE_BINDING_ANNOT1 + CONST_BINDING_ANNOT2,
        ('INSTALL_ANNOT1 + INSTALL_ANNOT2',) + INSTALL_ANNOT1 + INSTALL_ANNOT2,
        ('CONST_BINDING_FROM_INSTALL_ANNOT1 + INSTALL_ANNOT2',) + CONST_BINDING_FROM_INSTALL_ANNOT1 + INSTALL_ANNOT2,
        ('CONST_BINDING_ANNOT1 + INSTALL_ANNOT2',) + CONST_BINDING_ANNOT1 + INSTALL_ANNOT2,
        ('INSTALL_ANNOT1 + CONST_BINDING_FROM_INSTALL_ANNOT2',) + INSTALL_ANNOT1 + CONST_BINDING_FROM_INSTALL_ANNOT2,
        ('INSTALL_ANNOT1 + CONST_BINDING_ANNOT2',) + INSTALL_ANNOT1 + CONST_BINDING_ANNOT2,
        ('CONST_BINDING_FROM_INSTALL_ANNOT1 + CONST_BINDING_FROM_INSTALL_ANNOT2',) + CONST_BINDING_FROM_INSTALL_ANNOT1 + CONST_BINDING_FROM_INSTALL_ANNOT2,
        ('CONST_BINDING_ANNOT1 + CONST_BINDING_ANNOT2',) + CONST_BINDING_ANNOT1 + CONST_BINDING_ANNOT2,
        ('CONST_BINDING_ANNOT1 + CONST_BINDING_FROM_INSTALL_ANNOT2',) + CONST_BINDING_ANNOT1 + CONST_BINDING_FROM_INSTALL_ANNOT2,
    ])
    def test_no_clash_with_different_annotations(self, binding1_preparation, binding1, binding2_preparation, binding2):
        source = '''
            struct X {};
    
            %s
            %s
    
            Fruit::Component<const XAnnot1, const XAnnot2> getComponent() {
              return Fruit::createComponent()
                  %s
                  %s;
            }
    
            int main() {
                Fruit::Injector<const XAnnot1, const XAnnot2> injector(getComponent);
                injector.get<XAnnot1>();
                injector.get<XAnnot2>();
            }
            ''' % (binding1_preparation, binding2_preparation, binding1, binding2)
        expect_success(
            COMMON_DEFINITIONS,
            source)

    @parameterized.parameters([
        ('X', 'X', 'X'),
        ('const X', 'X', 'X'),
        ('X', 'const X', 'X'),
        ('const X', 'const X', 'X'),
        ('Fruit::Annotated<Annotation1, X>', 'Fruit::Annotated<Annotation1, X>', 'Fruit::Annotated<Annotation1, X>'),
        ('Fruit::Annotated<Annotation1, const X>', 'Fruit::Annotated<Annotation1, X>', 'Fruit::Annotated<Annotation1, X>'),
        ('Fruit::Annotated<Annotation1, X>', 'Fruit::Annotated<Annotation1, const X>', 'Fruit::Annotated<Annotation1, X>'),
        ('Fruit::Annotated<Annotation1, const X>', 'Fruit::Annotated<Annotation1, const X>', 'Fruit::Annotated<Annotation1, X>'),
    ])
    def test_during_component_merge(self, NormalizedComponentXAnnot, ComponentXAnnot, XAnnot):
        source = '''
            struct X {};
    
            Fruit::Component<NormalizedComponentXAnnot> getComponent1() {
              return Fruit::createComponent()
                .registerConstructor<XAnnot()>();
            }
    
            Fruit::Component<ComponentXAnnot> getComponent2() {
              return Fruit::createComponent()
                .registerConstructor<XAnnot()>();
            }
    
            void f() {
              Fruit::NormalizedComponent<NormalizedComponentXAnnot> nc(getComponent1);
              Fruit::Injector<> injector(nc, getComponent2);
              (void) injector;
            }
            '''
        expect_compile_error(
            'DuplicateTypesInComponentError<XAnnot>',
            'The installed component provides some types that are already provided',
            COMMON_DEFINITIONS,
            source,
            locals())

    def test_during_component_merge_with_different_annotation_ok(self):
        source = '''
            struct X {};
    
            Fruit::Component<XAnnot1> getComponent1() {
              return Fruit::createComponent()
                .registerConstructor<XAnnot1()>();
            }
    
            Fruit::Component<XAnnot2> getComponent2() {
              return Fruit::createComponent()
                .registerConstructor<XAnnot2()>();
            }
    
            int main() {
              Fruit::NormalizedComponent<XAnnot1> nc(getComponent1);
              Fruit::Injector<XAnnot1, XAnnot2> injector(nc, getComponent2);
              injector.get<XAnnot1>();
              injector.get<XAnnot2>();
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source)

    @parameterized.parameters([
        ('X', '(struct )?X'),
        ('Fruit::Annotated<Annotation1, X>', '(struct )?Fruit::Annotated<(struct )?Annotation1, ?(struct )?X>'),
    ])
    def test_bind_instance_and_bind_instance_runtime(self, XAnnot, XAnnotRegex):
        source = '''
            struct X {};
    
            Fruit::Component<> getComponentForInstanceHelper() {
              // Note: don't do this in real code, leaks memory.
              return Fruit::createComponent()
                .bindInstance<XAnnot, X>(*(new X()));
            }
            
            Fruit::Component<XAnnot> getComponentForInstance() {
              // Note: don't do this in real code, leaks memory.
              return Fruit::createComponent()
                .install(getComponentForInstanceHelper)
                .bindInstance<XAnnot, X>(*(new X()));
            }
    
            int main() {
              Fruit::Injector<XAnnot> injector(getComponentForInstance);
              injector.get<XAnnot>();
            }
            '''
        expect_runtime_error(
            'Fatal injection error: the type XAnnotRegex was provided more than once, with different bindings.',
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        ('X', '(struct )?X'),
        ('Fruit::Annotated<Annotation1, X>', '(struct )?Fruit::Annotated<(struct )?Annotation1, ?(struct )?X>'),
    ])
    def test_bind_instance_and_binding_runtime(self, XAnnot, XAnnotRegex):
        source = '''
            struct X {};
    
            Fruit::Component<> getComponentForInstanceHelper(X* x) {
              return Fruit::createComponent()
                .bindInstance<XAnnot, X>(*x);
            }
            
            Fruit::Component<XAnnot> getComponentForInstance(X* x) {
              return Fruit::createComponent()
                .install(getComponentForInstanceHelper, x)
                .registerConstructor<XAnnot()>();
            }
    
            int main() {
              X x;
              Fruit::Injector<XAnnot> injector(getComponentForInstance, &x);
              injector.get<XAnnot>();
            }
            '''
        expect_runtime_error(
            'Fatal injection error: the type XAnnotRegex was provided more than once, with different bindings.',
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        'X',
        'Fruit::Annotated<Annotation1, X>',
    ])
    def test_during_component_merge_consistent_ok(self, XAnnot):
        source = '''
            struct X : public ConstructionTracker<X> {
              using Inject = X();
            };
    
            Fruit::Component<XAnnot> getComponent() {
              return Fruit::createComponent();
            }
    
            Fruit::Component<> getRootComponent() {
              return Fruit::createComponent()
                  .install(getComponent);
            }
    
            int main() {
              Fruit::NormalizedComponent<> normalizedComponent(getRootComponent);
              Fruit::Injector<XAnnot> injector(normalizedComponent, getComponent);
    
              Assert(X::num_objects_constructed == 0);
              injector.get<XAnnot>();
              Assert(X::num_objects_constructed == 1);
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

if __name__ == '__main__':
    absltest.main()
