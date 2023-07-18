build image with:
> docker build -t smit_api .

run image with:
> docker run --name smit_containder -p 80:80 smit_api

> docker push kubanemil/smit_api

>docker pull kubanemil/smit_api

>docker run --name kuban_smit_api -p 80:80 kubanemil/smit_api

For this project, the API gets Tariff from the API itself, but in case that 
you need to retrieve Tariff from external API, you just need to set it as 
an environmental variable TARIFF_URL.

When you run docker, it will automatically create data, so you can just explore them
in API docs. Just get to /get_insurance endpoint and input COST and the cargo name to get it's 
insurance.

If you want to add more cargo, and specify it's rate by date, you can use /create_cargo endpoint.