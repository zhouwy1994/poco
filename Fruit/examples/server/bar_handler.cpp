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

#include "bar_handler.h"

#include <iostream>

using namespace std;
using namespace Fruit;

class BarHandlerImpl : public BarHandler {
private:
  const Request& request;
  const ServerContext& serverContext;

public:
  INJECT(BarHandlerImpl(const Request& request, const ServerContext& serverContext))
      : request(request), serverContext(serverContext) {}

  void handleRequest() override {
    cout << "BarHandler handling request on server started at " << serverContext.startupTime
         << " for path: " << request.path << endl;
  }
};

Component<Required<Request, ServerContext>, BarHandler> getBarHandlerComponent() {
  return Poco::Fruit::createComponent().bind<BarHandler, BarHandlerImpl>();
}
