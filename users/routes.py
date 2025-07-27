from flask import Blueprint, render_template, request,url_for,flash,redirect
from .forms import (ManunuziForm,BidhaaForm,MauzoForm,Mabadiliko_BeiForm,LipaForm,MapatoForm,MatumiziForm,
                    UzalishajiForm,MadeniForm,MpishiForm,StoreForm)
from Bakery.database import ManunuziData,Bidhaa,Uzalishaji,Mauzo,Madeni,Mpishi,Store,Mapato,Matumizi
from Bakery import db
from flask_login import login_required
from Bakery.authorization.validate import manunuzi_required, mauzo_required, mpishi_required, store_required

users = Blueprint('users', __name__)

@users.route('/manunuzi',methods=['GET','POST'])
@login_required
@manunuzi_required
def manunuzi():
    form = ManunuziForm()
    if form.validate_on_submit():
        mf = form.maligafi.data
        un = form.unit.data
        idadi = form.idadi.data
        jumla = idadi * form.bei.data
        manunuziData = ManunuziData(maligafi=mf,unit=un,idadi=idadi,bei=jumla)
        db.session.add(manunuziData)
        db.session.commit()
        
        return redirect(url_for('users.manunuzi'))
    else:

        manunuzidisp = ManunuziData.query.all()
        return render_template('manunuzi.html',manunuzidisp=manunuzidisp,form=form)
    
    

@users.route('/boss',methods=['GET','POST'])
def boss():
    return render_template('boss.html')

@users.route('/mauzo',methods=['GET','POST'])
@login_required
@mauzo_required
def mauzo():
    form = MauzoForm()
    
    if form.validate_on_submit():
        #mz means mauzo variable
        #create bei and foreign key from bidhaa
        bid_data = Bidhaa.query.filter_by(b_name=form.bid.data).first()
        mzs = Mauzo.query.filter_by(bid_id=bid_data.id).first()
        if mzs:
          baki = mzs.jumla - form.b_uza.data
          if baki >= 0:      
                bei = bid_data.b_bei * form.b_uza.data
                mzs.b_uza = form.b_uza.data
                mzs.b_bei_uza = bei 
                mzs.jumla = baki
                db.session.commit()
                return redirect(url_for('users.mauzo'))
          else:
                return f"Idadi iliyotoka {form.b_uza.data} ni kubwa kuliko kiasi kilichopo, Angalia kwa makini au wasiliana na Wahusika wa Uzalishaji"
        else:
            return f"Bidhaa hiyo bado haijaingia wasiliana na Wahusika wa Uzalishaji"
    else:
        #mzdisp for mauzo Query data
        mzdisp = Mauzo.query.order_by(Mauzo.id.desc()).all()
        return render_template('mauzo.html',form=form,title="Mauzo",mzdisp=mzdisp)

@users.route('/uzalishaji',methods=['GET','POST'])
@login_required
@mauzo_required
def uzalishaji():
    form = UzalishajiForm()
    if form.validate_on_submit():
        #uzal for uzalishaji variable and bid_data explained in mauzo route
        bid_data = Bidhaa.query.filter_by(b_name=form.bid.data).first()
        
        uzal = Uzalishaji(b_jumla = form.jumla.data, bid_id = bid_data.id)
        db.session.add(uzal)
        #db.session.commit()
        #update mauzo table with the new data
        mz = Mauzo.query.filter_by(bid_id=bid_data.id).first()
        if mz:
            mz.jumla = mz.jumla + form.jumla.data
            
        else:
            mauzo = Mauzo(jumla=form.jumla.data,bid_id=bid_data.id)
            db.session.add(mauzo)
        db.session.commit()
        #flash message
        flash('Data is Sent Successfully','primary')
        return redirect(url_for('users.uzalishaji'))
    else:
        #uzaldisp for displaying in uzalishaji.html
        uzaldisp = Uzalishaji.query.all()
        return render_template('uzalishaji.html',form=form,uzaldisp=uzaldisp)
        
@users.route('/bidhaa',methods=['POST','GET'])
@login_required
@mauzo_required
def bidhaa():

    form = BidhaaForm()
    if form.validate_on_submit():
        bid = Bidhaa(b_name=form.bidhaa.data,b_bei=form.bei.data)
        db.session.add(bid)
        db.session.commit()
        flash('New Entry Added','info')
        return redirect(url_for('users.bidhaa'))
    else:
        bid = Bidhaa.query.all()
        return render_template('bidhaa.html', form=form,bid=bid)
    
@users.route('/madeni',methods=['GET','POST'])
@login_required
@mauzo_required
def madeni():
    form = MadeniForm()
    collapse = False
    if form.validate_on_submit():
        # Get the selected product from the dropdown
        bid_data = Bidhaa.query.filter_by(b_name=form.bidhaa.data).first()
        baki = (bid_data.b_bei * form.idadi.data) - form.kiasi_kalipa.data

        #update number of product in Mauzo Table
        mz = Mauzo.query.filter_by(bid_id=bid_data.id).first()
        if mz:
            baki = mz.jumla - form.idadi.data
            if baki >= 0: 
                k_baki = (bid_data.b_bei * form.idadi.data) - form.kiasi_kalipa.data
                mz.jumla = baki
                md = Madeni(name=form.name.data, phone=form.phone.data, kiasi_kalipa=form.kiasi_kalipa.data, kiasi_baki=k_baki,status=form.idadi.data, bid_id=bid_data.id)
                db.session.add(md)
                db.session.commit()
                collapse = False
                flash('New Entry Added','info')
                return redirect(url_for('users.madeni'))
            else:
                return f"Idadi iliyotoka {form.idadi.data} ni kubwa kuliko kiasi kilichopo, Angalia kwa makini au wasiliana na Wahusika wa Uzalishaji"
        else:
            return f"Bidhaa hiyo bado haijaingia wasiliana na Wahusika wa Uzalishaji"
    else:
        collapse = False
        md = Madeni.query.order_by(Madeni.id.desc()).all()
        return render_template('madeni.html', form=form, md=md, collapse=collapse)


@users.route('/mpishi',methods=['GET','POST'])
@login_required
@mpishi_required
def mpishi():
    form = MpishiForm()
    if form.validate_on_submit():
        #loading bidhaa data
        bid_data = Bidhaa.query.filter_by(b_name=form.bid.data).first()
        
        #inserting data to the database
        mpishi = Mpishi(pondo=form.pondo.data, idadi=form.idadi.data,bid_id=bid_data.id)
        db.session.add(mpishi)
        db.session.commit()

        return redirect(url_for('users.mpishi'))
    else:

        #display on the screen 
        mpdsp = Mpishi.query.all()
        return render_template('mpishi.html', form=form, mpdsp=mpdsp)


@users.route('/store',methods=['GET','POST'])
@login_required
@store_required
def store():
    form = StoreForm()
    if form.validate_on_submit():

        #inserting data to the database
        store = Store(maligafi=form.maligafi.data, units=form.unit.data,idadi=form.idadi.data)
        db.session.add(store)
        db.session.commit()
        return redirect(url_for('users.store'))
    else:
        
        #display on the screen 
        strdsp = Store.query.all()
        return render_template('store.html', form=form, strdsp=strdsp)

@users.route('/B_bei/<int:id>',methods=['GET','POST'])
@login_required
@mauzo_required
def mabaliko_Bei(id):
    bid_data = Bidhaa.query.get_or_404(id)
    form = Mabadiliko_BeiForm()
    if form.validate_on_submit():
        bid_data.b_bei = form.bei.data
        db.session.commit()
        flash('Bei updated','info')
        return redirect(url_for('users.bidhaa'))
    else:
        return render_template('bei.html',form=form)
        

@users.route('/lipa/<int:id>',methods=['GET','POST'])
@login_required
@mauzo_required
def lipa(id):
    deni = Madeni.query.get_or_404(id)
    form = LipaForm()
    if form.validate_on_submit():
        deni.kiasi_kalipa = form.lipa.data + deni.kiasi_kalipa
        deni.kiasi_baki = (deni.bid.b_bei * deni.status) - deni.kiasi_kalipa
        db.session.commit()
        flash('Deni updated','info')
        return redirect(url_for('users.madeni'))
    else:
        return render_template('lipa.html',form=form)
    
@users.route('/mapato', methods=['GET', 'POST'])
def mapato():
    form = MapatoForm()
    if form.validate_on_submit():
        data = Mapato(kiasi=form.kiasi.data, maelezo=form.maelezo.data)
        db.session.add(data)
        db.session.commit()
        flash('Mapato yamehifadhiwa')
        return redirect(url_for('users.mapato'))
    return render_template('mapato.html', form=form)

@users.route('/matumizi', methods=['GET', 'POST'])
def matumizi():
    form = MatumiziForm()
    if form.validate_on_submit():
        data = Matumizi(kiasi=form.kiasi.data, aina=form.aina.data)
        db.session.add(data)
        db.session.commit()
        flash('Matumizi yamehifadhiwa')
        return redirect(url_for('users.matumizi'))
    return render_template('matumizi.html', form=form)
