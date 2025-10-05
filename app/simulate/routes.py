from datetime import datetime, timezone
from flask import render_template, flash, redirect, url_for, request, g, \
    current_app
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from langdetect import detect, LangDetectException
from app import db
from app.simulate.forms import DateForm, EmptyForm
from app.translate import translate
from app.simulate import bp
from app import mqtt
from app import socketio
from flask_socketio import emit, send


import pandas as pd
import plotly
import plotly.graph_objs as go

#import plotly.express as px
import json
from time import sleep

@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()
    g.locale = str(get_locale())


@bp.route('/simulate', methods=['GET', 'POST'])
@login_required
def simulate():
    form = DateForm()

    if form.validate_on_submit():
        current_user.selected_date = form.entrydate.data
        db.session.commit()
        flash(_('Date '+str(form.entrydate.data)+' is selected.'))
        return redirect(url_for('simulate.simulate'))
    elif request.method == 'GET':
        form.entrydate.data = current_user.selected_date
        

    df = pd.read_csv('.\\app\\static\\Data2023_clean.csv')
    keys = df.keys()
    clean_keys = [key.replace(" ", "") for key in keys]
    df.columns = clean_keys

    selected_date = current_user.selected_date
    
    if selected_date == None:
        selected_date=20230101
    else:
        selected_date = int(str(current_user.selected_date).replace("-","").split(" ")[0])
    df_date = df[df[df.keys()[1]]==selected_date]

    fig = [go.Scatter(x=df_date['HH'], y=df_date ['Q'], mode='lines', name='Sun', line=dict(width=4), yaxis='y1')]
    fig.append(go.Bar(x=df_date ['HH'], y=df_date ['APX'], name='APX', opacity=0.3, marker={'color': 'green'}, yaxis='y1'))
    fig.append(go.Scatter(x=[], y=[], mode='lines', name='HouseA', opacity=0.3, marker={'color': 'red'}, yaxis='y2'))

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    layout = json.dumps({'margin': dict(l=50, r=50, t=50, b=50),
                         'xaxis': dict(title='Time [hr]',
                                       tickmode = 'linear',
                                       dtick = 1.0),
                         'yaxis': dict(title='Solar intensity [W/m2] / APX price [EUR/MWh]',
                                   zeroline=True,
                                   zerolinewidth=2,
                                   range=[-100, 350]
 

                                   ),
                         'yaxis2': dict(title='Energy consumed [Wh]',
                                   overlaying='y',
                                   side='right',
                                   zeroline=True,
                                   zerolinewidth=2,
                                   showgrid=False,
                                   range=[-1, 3.5]
                                   
                                   ),
                          'legend': dict(
#                             #       orientation="v", 
#                                    bgcolor="Red",
                               #     yanchor="bottom", y=0.0, xanchor="left", x=0.02,
                                    borderwidth=1,
                                    bordercolor="Red",
                                       )
                          })
          
    return render_template('simulate/simulate.html', title=_('Simulation'), form=form, graphJSON=graphJSON, layout=layout, app_name=current_app.config['APP_NAME'])

@bp.route('/translate', methods=['POST'])
@login_required
def translate_text():
    data = request.get_json()
    return {'text': translate(data['text'],
                              data['source_language'],
                              data['dest_language'])}



@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    print('Mqtt message 1x received', message.payload)
    data = int(message.payload)
  #  print(data_list)
  #  data = {'ind':int(data_list[0]), 'val':float(data_list[1])}
    print(data)
#    socketio.emit('updateValue', {'data': data} )
    socketio.emit('updateValue', data)


@socketio.on('message')
def handleMessage(data):
    print('Message from client : ', data)
#    send(msg, broadcast=True)


@socketio.on('updateValue')
def handleUpdateValue():
    print('Message received on updateValue: ')
#    send(msg, broadcast=True)

@socketio.on('connect')
def test_connect():
    print('Client connected...')
    emit('my response', {'data': 'Connected'})
    emit('setInitial', 'qq')

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


@socketio.on('my_event')
def handleEvent(data):
    print('Message emitted via frontend SIO and received via serverside SIO and : ', data)
#    send(msg, broadcast=True)