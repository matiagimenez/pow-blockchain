# Infrastructure creation

```bash
BUCKET_NAME="tf_pow_blockchain"
PREFIX="cluster/state"
terraform init --reconfigure --backend-config "bucket=${BUCKET_NAME}" --backend-config "prefix=${PREFIX}"
terraform plan -lock=false
terraform apply -lock=false --auto-approve
```
