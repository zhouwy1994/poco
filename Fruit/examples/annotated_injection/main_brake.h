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

#ifndef MAIN_BRAKE_H
#define MAIN_BRAKE_H

#include "brake.h"

#include <Poco/Fruit/fruit.h>

// This type is not meaningful by itself, it's only used for annotated injection.
// This marks a the Brake instance that represents the main brake.
struct MainBrake {};

Poco::Fruit::Component<Poco::Fruit::Annotated<MainBrake, Brake>> getMainBrakeComponent();

#endif // MAIN_BRAKE_H
