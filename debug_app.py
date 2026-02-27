import app
print('app imported successfully')
print('index version in session state default: ', getattr(app.st.session_state, 'index_version', None))
