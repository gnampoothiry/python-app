Run application locally with python
1. Go to src folder and run python .\app.pu
2. Access the application from browser using url http://localhost:5000/api/v1/details

Docker image built and the image is available with the name as python-app:v2
docker run -p 80:5000 python-app:v2
App can be accessed from the local machine with the url as http://localhost/v1/details

Tag and push the image to the docker hub
========Kind Install====
Download kind binary and add it to the windows path

=======Clean up KIND Environment=====
1. List all clusters -> kind get clusters
2. Delete cluster -> kind delete cluster --name kind
===Kubectl====
Kubectl is the application that connects to Kubernetes clusters
Download kubectl exe and add it to the windows path
==================================KIND Cluster
Create Kind cluster with the following command
kind create cluster --name kind --config .\kind-config.yaml

=====Install ingress controller with helm chart as we are inside the firewall and does not have access to k8 repo
1. Download helm and add it to the windows path
2. helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
3. helm repo update

helm upgrade --install ingress-nginx ingress-nginx/ingress-nginx `
  --namespace ingress-nginx --create-namespace `
  --set controller.kind=DaemonSet `
  --set controller.hostPort.enabled=true `
  --set controller.hostPort.ports.http=80 `
  --set controller.hostPort.ports.https=443 `
  --set controller.ingressClassResource.enabled=true `
  --set controller.ingressClassResource.name=nginx `
  --set controller.ingressClass=nginx `
  --set controller.service.type=NodePort `
  --set controller.image.registry=docker-k8s.repo.ercot.com `
  --set controller.image.image=ingress-nginx/controller `
  --set controller.admissionWebhooks.patch.image.registry=docker-k8s.repo.ercot.com `
  --set controller.admissionWebhooks.patch.image.image=ingress-nginx/kube-webhook-certgen

Finally verify the controller is installed with the following command
kubectl -n ingress-nginx get pods -o wide

You should see the response as below
ingress-nginx-controller-b4f7df87d-wjt8g   1/1     Running   1 (68s ago)   23h   10.244.0.5   kind-control-plane   <none>           <none>

Deploying python app to the kubernetes
========================================
Deploying any application to a kubernetes cluster involves following steps
1. Deployment -> Deploying the image to the kubernetes by specifying number of required pods. This deploys the application to the required
                  pods. These pods will expose the service to the pods ports
2. Service -> This is required for load balancing and provide single port which will distribute the load to the available pods
              This is required as users connect to the individual pods
3. Ingress controller -> This is to rout the external request to the Service port. The external request will be served by the ingress and
                         it will rout the request to the service port which in turn redirected to the pod

These three steps can be individually set up with kubectl apply or can be done using the helm chart
1.  kubectl apply -f .\deploy.yaml
2.  kubectl apply -f .\service.yaml
3.  kubectl apply -f .\ingress.yaml
4.  

All the above steps can be done in a single step through helm chart. Under charts folder there is helm chart folder for python-app
deployment. Move to the folder and execute the following command to install the app using helm
1. helm install python-app -n python . --create-namespace

Un install the python app with the command
1. helm uninstall python-app -n python

=====Installing Argo cd

helm upgrade --install argocd argo/argo-cd -n argocd --create-namespace -f .\values-ercot-registry.yaml

verify all pods are installed correctly with the command
kubectl get pods -n argocd (All pods to be running)


====Getting initial password====
1. List the secrets in the name space
   kubectl get secrets -n argocd
2. List the secrets (Encoded)
   kubectl get secrets -n argocd argocd-initial-admin-secret -o yaml
3. Copy the password from the display and use browser to base64 decode
   Use admin / decoded base64 to login to the argo cd

Application Overview <br>
This application was created by following a Udemy tutorial focused on building a Python-based application for exploring the Backstage portal. The project serves as a hands-on learning exercise to understand Python application structure, API interactions, and integration with Backstage’s service catalog and developer portal ecosystem. It provides a foundational example that can be extended or customized for real-world use cases within the Backstage platform.






PS C:\learning\udemy\backstage-portal\python-app\charts\argocd> helm upgrade --install argocd argo/argo-cd -n argocd --create-namespace -f .\values-argo.yaml
Release "argocd" does not exist. Installing it now.
NAME: argocd
LAST DEPLOYED: Wed Mar 25 13:48:27 2026
NAMESPACE: argocd
STATUS: deployed
REVISION: 1
DESCRIPTION: Install complete
TEST SUITE: None
NOTES:
In order to access the server UI you have the following options:

1. kubectl port-forward service/argocd-server -n argocd 8080:443

    and then open the browser on http://localhost:8080 and accept the certificate

2. enable ingress in the values file `server.ingress.enabled` and either
      - Add the annotation for ssl passthrough: https://argo-cd.readthedocs.io/en/stable/operator-manual/ingress/#option-1-ssl-passthrough
      - Set the `configs.params."server.insecure"` in the values file and terminate SSL at your ingress: https://argo-cd.readthedocs.io/en/stable/operator-manual/ingress/#option-2-multiple-ingress-objects-and-hosts     


After reaching the UI the first time you can login with username: admin and the random password generated during the installation. You can find the password by running:

kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d

(You should delete the initial secret afterwards as suggested by the Getting Started Guide: https://argo-cd.readthedocs.io/en/stable/getting_started/#4-login-using-the-cli)
PS C:\learning\udemy\backstage-portal\python-app\charts\argocd> 



kubectl get pod argocd-dex-server-b5c94bb68-m4d5k -n argocd -o jsonpath='{range.spec.containers[*]}{.name}{" => "}{.image}{"`n"}{end}'