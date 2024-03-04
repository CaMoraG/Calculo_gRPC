import sys
from concurrent import futures
import grpc
import server_pb2 as spb2
import server_pb2_grpc as sgrpc


def sort_array(subarray):
    n = len(subarray)
    for i in range(n - 1):
        for j in range(n - i - 1):
            if subarray[j] > subarray[j + 1]:
                temp = subarray[j]
                subarray[j] = subarray[j + 1]
                subarray[j + 1] = temp

    return subarray


class SortService(sgrpc.SortServiceServicer):
    def SortArray(self, request, context):
        received_subarray = request.data
        print("Subarreglo recibido: ", received_subarray)

        sorted_subarray = sort_array(received_subarray)
        print("Subarreglo ordenado: ", sorted_subarray)

        return spb2.Array(data=sorted_subarray)


def serve(num_operationserver):
    puerto = 12345 + num_operationserver
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sgrpc.add_SortServiceServicer_to_server(SortService(), server)
    server.add_insecure_port("[::]:" + str(puerto))
    server.start()
    print("Servidor de operación "+str(num_operationserver)+" esperando conexiones...")
    server.wait_for_termination()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Uso correcto: ", sys.argv[0], " num_server")
        exit(1)
    num_operationserver = int(sys.argv[1])
    serve(num_operationserver)
