FROM minio/minio:latest

RUN microdnf install rsync

COPY policies/ /policies/
COPY entrypoint.sh ./
RUN chmod 755 entrypoint.sh

EXPOSE 9000
EXPOSE 9001

ENTRYPOINT [ "./entrypoint.sh" ]
