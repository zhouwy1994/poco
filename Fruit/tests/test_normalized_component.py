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
    using XAnnot1 = Poco::Fruit::Annotated<Annotation1, X>;

    struct Annotation2 {};
    using XAnnot2 = Poco::Fruit::Annotated<Annotation2, X>;
    '''

class TestNormalizedComponent(parameterized.TestCase):
    @parameterized.parameters([
        ('X', 'X', 'Y'),
        ('Poco::Fruit::Annotated<Annotation1, X>', 'ANNOTATED(Annotation1, X)', 'Poco::Fruit::Annotated<Annotation2, Y>'),
    ])
    def test_success_normalized_component_provides_unused(self, XAnnot, X_ANNOT, YAnnot):
        source = '''
            struct X {};
    
            struct Y {
              INJECT(Y(X_ANNOT)) {};
            };
    
            Poco::Fruit::Component<Poco::Fruit::Required<XAnnot>, YAnnot> getComponent() {
              return Poco::Fruit::createComponent();
            }
    
            Poco::Fruit::Component<XAnnot> getXComponent(X* x) {
              return Poco::Fruit::createComponent()
                .bindInstance<XAnnot, X>(*x);
            }
    
            int main() {
              Poco::Fruit::NormalizedComponent<Poco::Fruit::Required<XAnnot>, YAnnot> normalizedComponent(getComponent);
    
              X x{};
    
              Poco::Fruit::Injector<XAnnot> injector(normalizedComponent, getXComponent, &x);
              injector.get<XAnnot>();
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        ('X', 'X', 'Y'),
        ('Poco::Fruit::Annotated<Annotation1, X>', 'ANNOTATED(Annotation1, X)', 'Poco::Fruit::Annotated<Annotation2, Y>'),
    ])
    def test_success(self, XAnnot, X_ANNOT, YAnnot):
        source = '''
            struct X {};
    
            struct Y {
              INJECT(Y(X_ANNOT)) {};
            };
    
            Poco::Fruit::Component<Poco::Fruit::Required<XAnnot>, YAnnot> getComponent() {
              return Poco::Fruit::createComponent();
            }
    
            Poco::Fruit::Component<XAnnot> getXComponent(X* x) {
              return Poco::Fruit::createComponent()
                .bindInstance<XAnnot, X>(*x);
            }
    
            int main() {
              Poco::Fruit::NormalizedComponent<Poco::Fruit::Required<XAnnot>, YAnnot> normalizedComponent(getComponent);
    
              X x{};
    
              Poco::Fruit::Injector<YAnnot> injector(normalizedComponent, getXComponent, &x);
              injector.get<YAnnot>();
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        ('X', 'X', 'Y'),
        ('Poco::Fruit::Annotated<Annotation1, X>', 'ANNOTATED(Annotation1, X)', 'Poco::Fruit::Annotated<Annotation2, Y>'),
    ])
    def test_success_inline_component(self, XAnnot, X_ANNOT, YAnnot):
        source = '''
            struct X {};
    
            struct Y {
              INJECT(Y(X_ANNOT)) {};
            };
    
            Poco::Fruit::Component<Poco::Fruit::Required<XAnnot>, YAnnot> getComponent() {
              return Poco::Fruit::createComponent();
            }
            
            Poco::Fruit::Component<XAnnot> getAdditionalComponent(X* x) {
              return Poco::Fruit::createComponent()
                .bindInstance<XAnnot, X>(*x);
            }
    
            int main() {
              Poco::Fruit::NormalizedComponent<Poco::Fruit::Required<XAnnot>, YAnnot> normalizedComponent(getComponent);
    
              X x{};
    
              Poco::Fruit::Injector<YAnnot> injector(normalizedComponent, getAdditionalComponent, &x);
              injector.get<YAnnot>();
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        'X',
        'Poco::Fruit::Annotated<Annotation1, X>',
    ])
    def test_injector_from_normalized_component_unsatisfied_requirements(self, XAnnot):
        source = '''
            struct X {};
    
            Poco::Fruit::Component<Poco::Fruit::Required<XAnnot>> getComponent();
            Poco::Fruit::Component<> getEmptyComponent();
    
            int main() {
              Poco::Fruit::NormalizedComponent<Poco::Fruit::Required<XAnnot>> normalizedComponent(getComponent);
              Poco::Fruit::Injector<> injector(normalizedComponent, getEmptyComponent);
            }
            '''
        expect_compile_error(
            'UnsatisfiedRequirementsInNormalizedComponentError<XAnnot>',
            'The requirements in UnsatisfiedRequirements are required by the NormalizedComponent but are not provided by the Component',
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        ('X', 'const X'),
        ('Poco::Fruit::Annotated<Annotation1, X>', 'Poco::Fruit::Annotated<Annotation1, const X>'),
    ])
    def test_normalized_component_providing_nonconst_from_component_providing_const_error(self, XAnnot, ConstXAnnot):
        source = '''
            struct X {};
            
            Poco::Fruit::Component<XAnnot> getComponent();
    
            int main() {
              Poco::Fruit::NormalizedComponent<ConstXAnnot> normalizedComponent(getComponent);
              (void) normalizedComponent;
            }
            '''
        expect_generic_compile_error(
            r'no matching function for call to .Poco::Fruit::NormalizedComponent<ConstXAnnot>::NormalizedComponent\(Poco::Fruit::Component<XAnnot> \(&\)\(\)\).'
            r'|no matching constructor for initialization of .Poco::Fruit::NormalizedComponent<ConstXAnnot>.'
            r'|.Poco::Fruit::NormalizedComponent<ConstXAnnot>::NormalizedComponent.: no overloaded function could convert all the argument types'
            r'|.Poco::Fruit::NormalizedComponent<ConstXAnnot>::NormalizedComponent.: none of the .* overloads could convert all the argument types',
            COMMON_DEFINITIONS,
            source,
            locals())

    # TODO: we should probably return a more specific error here.
    @parameterized.parameters([
        ('X', 'Y'),
        ('Poco::Fruit::Annotated<Annotation1, X>', 'Poco::Fruit::Annotated<Annotation2, Y>'),
    ])
    def test_injector_from_normalized_component_nonconst_requirements_provided_as_const_error(self, XAnnot, YAnnot):
        source = '''
            struct X {};
            struct Y {};
            
            Poco::Fruit::Component<const XAnnot> getXComponent();
            
            void f(Poco::Fruit::NormalizedComponent<Poco::Fruit::Required<XAnnot>, YAnnot> normalizedComponent) {
              Poco::Fruit::Injector<YAnnot> injector(normalizedComponent, getXComponent);
            }
            '''
        expect_compile_error(
            'NonConstBindingRequiredButConstBindingProvidedError<XAnnot>',
            'The type T was provided as constant, however one of the constructors/providers/factories in this component',
            COMMON_DEFINITIONS,
            source,
            locals())

if __name__ == '__main__':
    absltest.main()
