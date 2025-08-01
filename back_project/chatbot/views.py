from django.shortcuts import render
from .serializer import ChatSessionSerializer, QuestionAnswerSerializer, MessageSerializer
from rest_framework.views import APIView
from sentence_transformers import SentenceTransformer
from rest_framework.response import Response
from rest_framework import status
from .models import QuestionAnswer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd 



model = SentenceTransformer('all-MiniLM-L6-v2')

class CargarembeddingsMasivos(APIView):
    def post(self, request):
        data = request.data.get('preguntas_respuestas',[])
        
        if not data:
            return Response({'error':'No se encontraron preguntas'}, status=status.HTTP_400_BAD_REQUEST)
        
        resultados = []
        
        for item in data:
            pregunta = item.get('pregunta')
            respuesta = item.get('respuesta')
            
            if not pregunta or not respuesta:
                return Response(
                    {'error':'Faltan datos'}, status=status.HTTP_400_BAD_REQUEST
                )
            embedding = model.encode(pregunta).tolist()
            
            preguntas_respuestas = QuestionAnswer(
                question = pregunta,
                answer = respuesta,
                embedding =embedding
            )
            preguntas_respuestas.save()
            
            resultados.append(QuestionAnswerSerializer(preguntas_respuestas).data)
            
        return Response({"Cargados" : resultados},status=status.HTTP_201_CREATED)   
    
    def get(self, request):
        preguntas_respuestas = QuestionAnswer.objects.all()
        serializer = QuestionAnswerSerializer(preguntas_respuestas, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class ResponderMesanjes(APIView):
    def post(self, request):
        data = request.data.get("pregunta", [])
        
        if not data:
            return Response({'Error': 'No hay Pregunta'}, status=status.HTTP_400_BAD_REQUEST)
        
        #Ya recibo el mensaje
        
        embedding_pregunta = model.encode(data)
        response = (CargarembeddingsMasivos.get(self, request))
        df_embaddings = pd.DataFrame(response.data)
        
        simil = df_embaddings
        
        ## Aca en este punto vamos  agenerar lka comparacion con el coseno para poder tener el mque mayor similitud dtenga de esta manera podremos obtener la mejor respuesta
        
        return Response(embedding_pregunta, status=status.HTTP_200_OK)

        
        
        
        
        

        
        

