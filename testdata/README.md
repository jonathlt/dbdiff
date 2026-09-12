starting containers to give access to testdata

cd testdata/pg-server-a`

if you see
```
permission denied while trying to connect to the docker API at unix:///var/run/docker.sock
```
sudo usermod -aG docker $USER

remove all docker containers if appropriate

docker rm -v -f $(docker ps -qa)

cd testdata/pg-server-a
remove data folder
sudo rm -r data
docker compose up -d
restore the test data
./restore.sh pg-server-a

cd ..
cd ..
cd testdata/pg-server-b

remove data folder
sudo rm -R data
docker compose up -d

restore the test data
./restore.sh pg-server-b