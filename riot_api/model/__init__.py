# Win rate predict model Func

def model(dic):
    import pickle
    import pandas as pd
    from lightgbm import LGBMClassifier, plot_importance
    from xgboost import XGBClassifier

    model = None

    with open('model.pkl', 'rb') as file:
        model = pickle.load(file)
    
    # columns titles create
    columns = list()
    keys = list(map(lambda x: [f'{x}', f'{x}score'], range(1,11)))
    list(map(lambda x : columns.extend(x), keys))
    
    # DataFrame create
    df = pd.DataFrame(columns = doc)
    input_data = {key: value for key, value in zip(doc, dic)}

    # model predict
    X_test = df.append(input_data, ignore_index=True)
    X_test = X_test.astype(int)
    y_pred = list(model.predict(X_test))[0]
    c=model.predict_proba(X_test).reshape(-1,1)

    blue_team = int(list(c[0])[0]*100)
    red_team = int(list(c[1])[0]*100)

    if y_pred == 200:
        y_pred = '레드팀'
    else:
        y_pred = '블루팀'
    m = f'예상승리팀 : {y_pred},{"     "}블루팀={blue_team}%, 레드팀{red_team}%'

    return m