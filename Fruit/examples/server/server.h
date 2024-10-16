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

#ifndef SERVER_H
#define SERVER_H

#include "request.h"
#include "request_dispatcher.h"
#include "server_context.h"

#include <Poco/Fruit/fruit.h>
#include <string>

class Server {
public:
  virtual void run(Poco::Fruit::Component<Poco::Fruit::Required<Request, ServerContext>, RequestDispatcher> (
      *getrequestDispatcherComponent)()) = 0;
};

Poco::Fruit::Component<Server> getServerComponent();

#endif // SERVER_H
