from django.views.decorators.http import require_POST
from core.query import DB
import json
from LLMs.model_service import ModelService
# Create your views here.

from core import Blueprint,R,utils
router = Blueprint("commons")

@router.route('/wenti', methods=['POST'])
@require_POST
def wenti(request):
    try:
        data = json.loads(request.body)
        content = data.get('question')
        user_id = data.get('user_id')
        
        if not content:
            return R.error('问题内容不能为空')
            
        if not user_id:
            return R.error('用户ID不能为空')
            
        historyIds = []  # 暂时不使用历史记录
        historyIds.append(0)
        
        # 初始化大模型服务
        model_service = ModelService()
        
        # 首先尝试从数据库获取答案
        lists = (DB.name("Wenda")
            .where("jiansuoleixing", "精准")
            .where("tiwenneirong", content)
            .select())
        if len(lists):
            ids = [r.id for r in lists]
            huida = getHuida(ids,historyIds)
            if huida:
                # 获取数据库答案
                db_answer = huida.huidaneirong
                # 使用大模型优化答案
                enhanced_answer = model_service.answer_question(
                    question=content,
                    user_id=user_id,
                    context=f"原始答案：{db_answer}\n请基于这个答案，给出更详细、更准确的回答："
                )
                # 如果大模型返回空，使用原始答案
                if not enhanced_answer:
                    enhanced_answer = db_answer
                return R.success({'answer': enhanced_answer})
            
        lists = (DB.name('Wenda')
                .where("jiansuoleixing", "模糊")
                .where("LOCATE('"+content+"',tiwenneirong)>0 OR LOCATE(tiwenneirong,'"+content+"')>0")
                .select())
        if len(lists):
            ids = [r.id for r in lists]
            huida = getHuida(ids,historyIds)
            if huida:
                # 获取数据库答案
                db_answer = huida.huidaneirong
                # 使用大模型优化答案
                enhanced_answer = model_service.answer_question(
                    question=content,
                    user_id=user_id,
                    context=f"原始答案：{db_answer}\n请基于这个答案，给出更详细、更准确的回答："
                )
                # 如果大模型返回空，使用原始答案
                if not enhanced_answer:
                    enhanced_answer = db_answer
                return R.success({'answer': enhanced_answer})

        # 如果数据库中没有匹配的答案，直接使用大模型生成回答
        ai_answer = model_service.answer_question(
            question=content,
            user_id=user_id,
            context=""
        )

        if not ai_answer:
            ai_answer = "我还没学会怎么回答呢"
        return R.success({'answer': ai_answer})
    except json.JSONDecodeError:
        return R.error('无效的请求格式', code=400)
    except Exception as e:
        return R.error('服务器内部错误', code=500)

def getHuida(ids,historyIds):
    select = (DB.name('Huida')
            .where("wenti", "in", ids)
            .where("id", "not in", historyIds)
            .order("huidacishu asc")
            .order("rand()")
            .limit(1)
            .select())
    if len(select):
        huida = select[0]
        return updateHuida(huida)

    select = (DB.name('Huida')
            .where("wenti", "in", ids)
            .order("huidacishu asc")
            .order("rand()")
            .limit(1)
            .select())
    if len(select):
        huida = select[0]
        return updateHuida(huida)

    return False

def updateHuida(huida):
    huida.huidacishu = huida.huidacishu + 1
    DB.name("huida").where("id", huida.id).setInc("huidacishu")
    return huida

def sendContent(content, huida, enhanced_answer=None):
    (DB.name("wendaxiaoxi")
        .data("xiaoxineirong", content)
        .data("huifuneirong", enhanced_answer if enhanced_answer else huida.huidaneirong)
        .data("guanlianhuifu", huida.id)
        .data("yonghu", utils.session('username'))
        .insert())

    res = {
        'id': huida.id,
        'msg': enhanced_answer if enhanced_answer else huida.huidaneirong,
        'addtime': utils.getDateStr(),
    }

    return R.success(res)

def sendContentNull(content, huida):
    (DB.name("wendaxiaoxi")
        .data("xiaoxineirong", content)
        .data("huifuneirong", huida)
        .data("guanlianhuifu", 0)
        .data("yonghu", utils.session('username'))
        .insert())

    res = {
        'id': 0,
        'msg': huida,
        'addtime': utils.getDateStr(),
    }

    return R.success(res)