from trakt import init
import trakt.core
trakt.core.AUTH_METHOD = trakt.core.OAUTH_AUTH
print(init('falconsensei'))
# init('falconsensei', client_id='4f8cfb527d3bb478edb94e07a9c83917cf689b0f93ade1315601e2dcf693451a', client_secret='d7bd3ad8013ed5a312a3697146d5a491ade6ca1837fba53c95e42f8fa0d5dc5a')