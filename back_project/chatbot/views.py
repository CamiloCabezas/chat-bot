from django.shortcuts import render
from .serializer import ChatSessionSerializer, QuestionAnswerSerializer, MessageSerializer
from rest_framework.views import APIView
from sentence_transformers import SentenceTransformer
from rest_framework.response import Response
from rest_framework import status
from .models import QuestionAnswer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd 
from rest_framework.permissions import AllowAny


# model = SentenceTransformer('distiluse-base-multilingual-cased-v1')
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
    permission_classes = [AllowAny]
    
    def post(self, request):
        data = request.data.get("pregunta", [])
        print(data)
        if not data:
            return Response({'Error': 'No hay Pregunta'}, status=status.HTTP_400_BAD_REQUEST)
        
        #Ya recibo el mensaje
        
        embedding_pregunta = model.encode(data)
        response = (CargarembeddingsMasivos.get(self, request))
        df_embaddings = pd.DataFrame(response.data)
        
        simil = df_embaddings['embedding'].apply(lambda x: cosine_similarity([embedding_pregunta],[x])[0][0])
        
        if max(simil) < 0.65:
            return Response("No he entendido tu pregunta")
        
        index_max = simil.idxmax()
        
        respuesta = df_embaddings.loc[index_max, 'answer']
      
        # Ya aca estaria generando toda la logica de responder segun la base de datos que tenemos, ahora necesitariamos es ver como se comporta en el front
        
        return Response(respuesta, status=status.HTTP_200_OK)

        
        
        
        
        

        
        

