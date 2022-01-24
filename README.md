# MSI


k8s-iseze backend game server (used to store data about the scoreboard). This setup is ment to run on Azure. Before being able to kubectl apply -k ./k8s you have to create a registry secret (in my case registry-secret) to pull images from docker hub, secret for managing storage account (in my case azure-secret) and then you should be good to go. It is asummed you already have a working cluster (ingress controler,dns...). 

The final setup is describet in final_setup.txt. So we have an ingress rule that forwards all the trafic to the app service that is wrapped around pods in app deployment that uses a redis cache and a mysql database to stor its data. Volumes are used in mysql database so that in case of failure, the data stays intact. liveprobes are present in main app by trying to fetch data from /pridobi. If pod returns 4XX or 5XX it is considered dead/unheathy and it should will be restarted.

I used file-shares in Azure as volumes for mysql database and I am not really happy with the speed at which the new mysql pod is generated (1-2 mins).
