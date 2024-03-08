from concurrent import futures
import grpc
import server_pb2 as spb2
import server_pb2_grpc as sgrpc

operationServer1 = 'localhost:12346'
operationServer2 = 'localhost:12347'


# Envío de un subarreglo a un servidor de operación
def send_subarray(os, subarray):
    with grpc.insecure_channel(os) as channel:
        stub = sgrpc.SortServiceStub(channel)
        subarray = stub.SortArray(spb2.Array(data=subarray))
    return subarray.data


# Envio de los subarreglos a los servidores de operacion con tolerancia a fallos
def divide(top, bottom):
    try:
        top = send_subarray(operationServer1, top)
    except grpc.RpcError as e:
        print("Error OperationServer1: ", e)
        top = send_subarray(operationServer2, top)
    try:
        bottom = send_subarray(operationServer2, bottom)
    except grpc.RpcError as e:
        print("Error OperationServer2: ", e)
        bottom = send_subarray(operationServer1, bottom)

    return top, bottom


def joint_arrays(arr1, arr2):
    i = j = 0
    final_array = []
    while i < len(arr1) and j < len(arr2):
        if arr1[i] < arr2[j]:
            final_array.append(arr1[i])
            i += 1
        else:
            final_array.append(arr2[j])
            j += 1

    while i < len(arr1):
        final_array.append(arr1[i])
        i += 1

    while j < len(arr2):
        final_array.append(arr2[j])
        j += 1

    return final_array


class SortService(sgrpc.SortServiceServicer):
    def DivideAndMerge(self, request, context):
        # Conversion de los datos a un arreglo de python
        received_array = request.data
        print("Arreglo recibido: ", received_array)

        middle = len(received_array) // 2
        top = received_array[:middle]
        bottom = received_array[middle:]

        results = divide(top, bottom)
        sorted_array = joint_arrays(results[0], results[1])
        print("Arreglo ordenado: ", sorted_array)

        # Envío del arreglo al cliente convertido a un arreglo soportado por el rpc
        return spb2.Array(data=sorted_array)


def serve():
    # Creacion del servidor
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sgrpc.add_SortServiceServicer_to_server(SortService(), server)
    server.add_insecure_port("[::]:12345")
    server.start()
    print("Servidor de cálculo esperando conexiones...")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
