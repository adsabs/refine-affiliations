export RABBITMQ_NODE_PORT=5673
./rabbitmq-server/sbin/rabbitmq-server -detached
./rabbitmq-server/sbin/rabbitmqctl status

sleep 2