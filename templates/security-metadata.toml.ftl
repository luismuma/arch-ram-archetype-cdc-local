<#assign safeNniiIds = nniiIds![]>
nnii_ids = [<#list safeNniiIds as id>${id}<#if id_has_next>, </#if></#list>]
driving_entity = "${drivingEntity!""}"
project_name = "${projectName!""}"
project_lead = "${projectLead!""}"