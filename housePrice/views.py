# Create your views here.
# coding:utf-8

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from django.http import request
from django.http.response import HttpResponse
from django.http.response import JsonResponse
from django.shortcuts import render

from crawl.dataScore.dataMongo import detailList, Add_ComList, myMongo, mySFUN
from dataAlalyze.indexClean import runClean,result_refer


# 参考页面
def referInfo(request):
    return render(request, 'referInfo.html', {'list': Add_ComList})


# 跳转页面
def skipInfo(request, id):
    detai_dt = dict(myMongo.find()[id]).values()
    detai_dt = list(detai_dt)
    print(detai_dt)
    return render(request, 'itemdetailInfo.html', {'detai_dt': detai_dt})

# 500 处理
def server_error(request):
    return render(request, '500处理.html')


def empty_test_page(request):
    return render(request, 'fakerLAT.html')


def homePage(request):
    # 业务逻辑代码
    return render(request, 'AImap.html')


# 房价预测
def houseForecast(request):
    # 业务逻辑代码
    if request.method == 'GET':
        return render(request, 'priceDiv.html')
    elif request.method == 'POST':
        # 用来接受页面单个值，用request.POST.get
        # room,hall,restroom,houseSize,elevator,decorate,houseAge,SingelHouse,cAa,东
        decorateGet = request.POST['decoratetxt']
        housetypeGet = request.POST['housetypetxt']
        housesizeGet = request.POST['buildareatxt']
        liftGet = request.POST['lifttxt']
        totalfloorGet = request.POST['totalfloortxt']
        floorGet = request.POST['floortxt']
        rightGet = request.POST['righttxt']
        cAaGet = request.POST['addresstxt']
        towardGet = request.POST['towardtxt']
        singleGet = request.POST['singletxt']
        resList = [cAaGet, towardGet, housetypeGet, liftGet, floorGet, rightGet, decorateGet, housesizeGet,
                   totalfloorGet, singleGet]
        result_refer1 = result_refer(cAaGet)
        resList1 = runClean(resList)
        cAaGet = str(cAaGet).strip('－')
        # return render(request, 'priceDiv.html')
        return render(request, "resInfo.html", {'list': resList1[0], 'addressPoint': cAaGet,'result_refer':result_refer1})


# 安居客
def list_(request):
    # 业务逻辑代码
    # community,ApartmentTpye,perPrice,address,houseSize
    a = []
    # 一百条
    for i in myMongo.find()[:100]:
        d = dict(i)
        a.append(list(d.values()))
    # data = pd.read_csv('..\crawl\Anjuke\Anjuke1.csv')

    paginator = Paginator(a, 25)  # Show 25 contacts per page
    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            pages1 = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            pages1 = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            pages1 = paginator.page(paginator.num_pages)

        # return render(request, 'list.html', {'contacts': contacts})

    return render(request, 'listinfo.html', {'pages1': pages1})


# 房天下
def listSFUN(request):
    # 业务逻辑代码
    # community,ApartmentTpye,perPrice,address,houseSize
    a = []
    # 一百条
    for i in mySFUN.find()[:100]:
        d = dict(i)
        a.append(list(d.values()))
    # data = pd.read_csv('..\crawl\Anjuke\Anjuke1.csv')

    paginator = Paginator(a, 25)  # Show 25 contacts per page
    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            pages1 = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            pages1 = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            pages1 = paginator.page(paginator.num_pages)

        # return render(request, 'list.html', {'contacts': contacts})

    return render(request, 'listinfoSfun.html', {'pages1': pages1})


def baiduLNTLat(request):
    # 查询经纬度

    return render(request, template_name="经纬度.html")


def baiduConstruction(request):
    return render(request, template_name="基设.html")


def ajax_post(request):
    # return render(request, 'ajaxDeom.html', {'TutorialList': detailList})
    return render(request, 'ajaxDeom.html', {'TutorialList': detailList})


# 获得基建

def getConInfo(request):
    if request.method == 'POST':
        cont = request.POST
        print(cont)
        # body = json.loads(request.body)
        # print(body)
        return HttpResponse(cont)


def get_house_location(request):
    """
    该方法返回楼房的简要地理位置
    get 方法，访问该路径可以获取数据库中的地理位置 返回类型为json
    :param request:
    :return:
    """
    # TODO 访问数据库内容，获取地理位置， 构造字典返回 {"localtion": [你的地理位置]}
    # TODO 使用返回以便js使用
    location = {}
    location['address'] = detailList
    return JsonResponse({'location': detailList})


# # 获得基建
# def getConInfo(request):
#     if request.method == 'POST':
#         value = request.POST
#
#     return render(request,'postMyConInfo.html')

# 接受用户 csv输入
def get_csv_toHtml(requset):
    if request.method == 'GET':
        return render(request, 'dataList.html')

    elif request.method == 'POST':
        # u e sex city 都是用来接受页面单个值，用request.POST.get

        # f 用来接受文件request.FILES.get
        f = request.FILES.get('w')
        # request.FILES.get <InMemoryUploadedFile'>,f.name 是调用文件名
        with open(f.name, 'wb') as fi:
            # chunks 是上传的文件内容
            for i in f.chunks():
                fi.write(i)
        return render(request, 'dataList.html')
    else:
        return render(request, 'otherdataList.html')
