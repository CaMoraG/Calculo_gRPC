import grpc
import server_pb2 as spb2
import server_pb2_grpc as sgrpc


def run(array):
    print("Arreglo sin ordenar: ", array)
    with grpc.insecure_channel('localhost:12345') as channel:
        stub = sgrpc.SortServiceStub(channel)
        response = stub.DivideAndMerge(spb2.Array(data=array))
        print("Arreglo ordenado:", response.data)


def initialize_array():
    n = int(input("Ingrese el tamaño del arreglo: "))
    array = []
    print("Introduzca los numeros del arreglo de tamaño ", n)

    for i in range(n):
        m = int(input())
        array.append(m)

    run(array)


if __name__ == '__main__':
    initialize_array()
