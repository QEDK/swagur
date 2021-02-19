from django import forms
from django.http import HttpResponse
from django.shortcuts import render
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

transport = RequestsHTTPTransport(url="https://api.thegraph.com/subgraphs/name/protofire/augur-v2", verify=True,
    retries=3)
client = Client(transport=transport, fetch_schema_from_transport=True)

def userquery(user_id):
    return client.execute(gql('''{
      user(id: \"''' + user_id + '''\") {
        userTokenBalances(first: 100) {
          token {
            id,
            tokenType
          },
          balance
        },
        marketsCreated(first: 100) {
          id,
          timestamp,
          status,
          description
        }
      }
    }'''))

def marketquery(market_id):
    return client.execute(gql('''{
      market (id: \"''' + market_id + '''\") {
        timestamp,
        creator {
          id
        },
        owner {
          id
        },
        description,
        longDescription,
        status,
        marketType
      }
    }'''))

def index(request):
    return render(request, "augur/index.html")

def user(request):
    if request.method == "GET":
        return HttpResponse("App is running")
    elif request.method == "POST":
        return HttpResponse(str(userquery(request.POST["user_id"])))

def market(request):
    if request.method == "GET":
        return HttpResponse("App is running")
    elif request.method == "POST":
        return HttpResponse(str(marketquery(request.POST["market_id"])))
