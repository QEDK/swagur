from datetime import datetime
from django import forms
from django.http import HttpResponse
from django.shortcuts import render
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

transport = RequestsHTTPTransport(url="https://api.thegraph.com/subgraphs/name/protofire/augur-v2")
client = Client(transport=transport, fetch_schema_from_transport=True)

def userquery(user_id):
    return client.execute(gql('''{
      user(id: \"''' + user_id + '''\") {
        id,
        userTokenBalances(first: 100) {
          token {
            id,
            tokenType
          },
          balance
        },
        marketsCreated(first: 100) {
          id,
          status,
          description
        }
      }
    }'''))

def marketquery(market_id):
    return client.execute(gql('''{
      market (id: \"''' + market_id + '''\") {
        id,
        timestamp,
        endTimestamp,
        creator {
          id
        },
        owner {
          id
        },
        designatedReporter {
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
        result = userquery(request.POST["user_id"])["user"]
        return render(request, "augur/user.html", context={"result": result})

def userid(request, id):
    if request.method == "GET":
        result = userquery(id)
        return render(request, "augur/user.html", context={"result": result["user"]})

def market(request):
    if request.method == "GET":
        return HttpResponse("App is running")
    elif request.method == "POST":
        result = marketquery(request.POST["market_id"])["market"]
        result["timestamp"] = datetime.utcfromtimestamp(int(result["timestamp"])).strftime("%Y-%m-%d %H:%M:%S")
        result["endTimestamp"] = datetime.utcfromtimestamp(int(result["endTimestamp"])).strftime("%Y-%m-%d %H:%M:%S")
        return render(request, "augur/market.html", context={"market": result})

def marketid(request, id):
    if request.method == "GET":
        result = marketquery(id)["market"]
        result["timestamp"] = datetime.utcfromtimestamp(int(result["timestamp"])).strftime("%Y-%m-%d %H:%M:%S")
        result["endTimestamp"] = datetime.utcfromtimestamp(int(result["endTimestamp"])).strftime("%Y-%m-%d %H:%M:%S")
        return render(request, "augur/market.html", context={"market": result})
