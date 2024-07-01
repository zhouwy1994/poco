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

    struct Annotation1 {};
    using XAnnot1 = Fruit::Annotated<Annotation1, X>;

    struct Annotation2 {};
    using XAnnot2 = Fruit::Annotated<Annotation2, X>;
    '''

class TestComponent(parameterized.TestCase):
    @parameterized.parameters([
        'X',
        'Fruit::Annotated<Annotation1, X>',
    ])
    def test_move(self, XAnnot):
        source = '''
            struct X {
              using Inject = X();
            };
    
            Fruit::Component<XAnnot> getComponent() {
              Fruit::Component<XAnnot> c = Fruit::createComponent();
              Fruit::Component<XAnnot> c2 = std::move(c);
              return Fruit::Component<XAnnot>(std::move(c2));
            }
    
            int main() {
              Fruit::Injector<XAnnot> injector(getComponent);
              injector.get<XAnnot>();
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        'X',
        'Fruit::Annotated<Annotation1, X>',
    ])
    def test_move_partial_component(self, XAnnot):
        source = '''
            struct X {
              using Inject = X();
            };
    
            Fruit::Component<XAnnot> getComponent() {
              auto c = Fruit::createComponent();
              auto c1 = std::move(c);
              return std::move(c1);
            }
    
            int main() {
              Fruit::Injector<XAnnot> injector(getComponent);
              injector.get<XAnnot>();
            }
            '''
        expect_generic_compile_error(
            r'error: use of deleted function .Fruit::PartialComponent<Bindings>::PartialComponent\(Fruit::PartialComponent<Bindings>&&\).'
            r'|error: call to deleted constructor of .(Fruit::)?PartialComponent<>.'
            # MSVC 2017
            r'|error C2280: .Fruit::PartialComponent<>::PartialComponent\(Fruit::PartialComponent<> &&\).: attempting to reference a deleted function'
            # MSVC 2015
            r'|error C2248: .Fruit::PartialComponent<>::PartialComponent.: cannot access private member declared in class .Fruit::PartialComponent<>.',
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        ('X', 'X'),
        ('X', 'const X'),
        ('Fruit::Annotated<Annotation1, X>', 'Fruit::Annotated<Annotation1, X>'),
        ('Fruit::Annotated<Annotation1, X>', 'Fruit::Annotated<Annotation1, const X>'),
    ])
    def test_error_no_binding_found(self, XAnnot, ConstXAnnot):
        source = '''
            struct X {};
    
            Fruit::Component<ConstXAnnot> getComponent() {
              return Fruit::createComponent();
            }
            '''
        expect_compile_error(
            'NoBindingFoundError<XAnnot>',
            'No explicit binding nor C::Inject definition was found for T.',
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        ('X', 'X'),
        ('X', 'const X'),
        ('Fruit::Annotated<Annotation1, X>', 'Fruit::Annotated<Annotation1, X>'),
        ('Fruit::Annotated<Annotation1, X>', 'Fruit::Annotated<Annotation1, const X>'),
    ])
    def test_error_no_binding_found_abstract_class(self, XAnnot, ConstXAnnot):
        source = '''
            struct X {
              virtual void f() = 0;
            };
    
            Fruit::Component<ConstXAnnot> getComponent() {
              return Fruit::createComponent();
            }
            '''
        expect_compile_error(
            'NoBindingFoundForAbstractClassError<XAnnot,X>',
            'No explicit binding was found for T, and note that C is an abstract class',
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        '',
        'const',
    ])
    def test_error_no_factory_binding_found(self, MaybeConst):
        source = '''
            struct X {};
    
            Fruit::Component<MaybeConst std::function<std::unique_ptr<X>()>> getComponent() {
              return Fruit::createComponent();
            }
            '''
        expect_compile_error(
            r'NoBindingFoundError<std::function<std::unique_ptr<X(,std::default_delete<X>)?>\((void)?\)>',
            'No explicit binding nor C::Inject definition was found for T.',
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        '',
        'const',
    ])
    def test_error_no_factory_binding_found_with_annotation(self, MaybeConst):
        source = '''
            struct X {};
    
            Fruit::Component<Fruit::Annotated<Annotation1, MaybeConst std::function<std::unique_ptr<X>()>>> getComponent() {
              return Fruit::createComponent();
            }
            '''
        expect_compile_error(
            r'NoBindingFoundError<Fruit::Annotated<Annotation1,std::function<std::unique_ptr<X(,std::default_delete<X>)?>\((void)?\)>>',
            'No explicit binding nor C::Inject definition was found for T.',
            COMMON_DEFINITIONS,
            source,
            locals())

if __name__ == '__main__':
    absltest.main()
