########
# Copyright (c) 2014 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
#    * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    * See the License for the specific language governing permissions and
#    * limitations under the License.


from cloudify import ctx
from cloudify.decorators import operation


@operation(resumable=True)
def handle_capabilities(ctx):

    requirements = ctx.source.node.properties['requirements']
    capabilities = ctx.target.node.properties['capabilities']
    
    for capability in capabilities:
        ctx.source.instance.runtime_properties[requirements[capability]] = \
            ctx.target.instance.runtime_properties.get(capabilities[capability], 
                                                       None)
        ctx.source.instance.update()
        
        # If runtime_capability from target node is None, the configuration
        # in blueprint could be invalid.
        if ctx.source.instance.runtime_properties[requirements[capability]] is None:
            ctx.logger.info(
                'Could not find capability \'{}\''.format(str(capability))
                )
