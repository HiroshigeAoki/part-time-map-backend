from fastapi import status, HTTPException
from pydantic import BaseModel, Field, root_validator, validate_arguments
from geojson import Point
from typing import Dict, Literal, List
import geocoder

class Commute(BaseModel):
    travelMode: Literal['WALKING', 'BICYCLING','DRIVING', 'TRANSIT'] = Field(None, description='https://developers.google.com/maps/documentation/javascript/directions#TravelModes')
    time: Literal['5分', '10分', '20分', '30分'] = Field(None, description='通勤時間。選択肢は仮。')
    
    @root_validator
    def is_both_filled(cls, v):
        if not all(v.values()):
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='Both transp and time is required if either one is filled.')
        return v

class Query(BaseModel):
    origins: Dict = Field(description='{"lat": -180<=lng<=180, "lng": -90<=lat<=90}')
    # radius: Literal['300m', '500m', '1km', '2km', '3km', '5km', '10km', '15km', '20km', '30km'] = Field('2km', description='radiusかcoummuteどちらか一つのみ。')
    commute: Commute = Field(None)
    jc: List[Literal["飲食/フード", "販売", "接客/サービス", "レジャー/エンタメ", "営業", "事務", "総務/企画", "教育", "物流/配送", "軽作業", "建築/土木/建設", "工場/製造", "IT/コンピュータ", "医療/介護/福祉", "マスコミ/出版", "芸能", "ガールズバー/キャバクラ/パブ/クラブ", "専門職/その他"]] = Field(None, description='職種')
    jmc: List[
        Literal[
            "ファミレス・レストラン(ホールスタッフ)", "居酒屋（ホールスタッフ)", "その他飲食店(ホールスタッフ)", "キッチンスタッフ(ファミレス・レストラン)", "キッチンスタッフ(居酒屋)", "キッチンスタッフ(その他飲食店)", "ファーストフード", "カフェ・喫茶店", "宅配・デリバリー", "食品製造・販売", "飲食店(店長・マネージャー)", "パン屋（ベーカリー）", "ケーキ屋・スイーツ", "焼肉屋", "うどん・蕎麦屋", "寿司屋・回転寿司", "ラーメン屋", "ビアガーデン", "弁当屋", "惣菜・デリ・デパ地下", "ピザ屋", "フードコート", "バー（BAR）・バーテンダー", "皿洗い・洗い場", "配膳", "その他飲食/フード", 
            "コンビニ", "レジ", "家電量販店・携帯販売（携帯ショップ）", "インテリア・雑貨販売", "ドラッグストア・薬局・化粧品販売", "DPE･カメラ店スタッフ", "レンタルビデオ・CD", "アパレル", "ファッションデザイナー・パタンナー", "バイヤー", "試食試飲・デモンストレーター・マネキン", "スタイリスト", "販売店(店長・マネージャー)", "書店・本屋", "CD・DVD販売", "ペットショップ", "スーパー", "花屋（フラワーショップ）", "100円ショップ", "ホームセンター", "グッズ販売", "その他販売", 
            "警備員・監視員", "清掃員・掃除", "クリーニング・洗浄", "ビルメンテナンス（ビル管理・設備管理他）", "ガソリンスタンド", "パーキングスタッフ", "ポスティング・チラシ配り", "サンプリング・ティッシュ配り", "冠婚葬祭関連（ブライダル・結婚式場他）", "ベビーシッター", "家事代行", "洗車", "サービス関連派遣職", "サービス業(店長・マネージャー)", "その他サービス", 
            "イベントスタッフ・コンサートスタッフ", "パチンコ", "カラオケ", "アミューズメントスタッフ", "インストラクター", "フロント・受付", "ホテルスタッフ（フロント等）", "ベッドメイキング", "その他宿泊施設業務", "ゴルフ場（キャディ）", "ペンション・旅館・民宿スタッフ", "漫画喫茶・ネットカフェ", "映画館", "スキー場", "レンタカー", "温泉・銭湯・スーパー銭湯", "プール監視員", "レジャー施設(店長・マネージャー)", "その他レジャー", 
            "営業・企画営業（法人対象）", "営業・企画営業（個人対象）", "ルートセールス", "営業アシスタント", "テレフォンアポインター（テレアポ）", "新聞社", "営業関連派遣職", "その他営業", 
            "一般事務", "経理事務", "営業事務", "貿易事務", "伝票整理・資料作成", "電話応対", "コールセンター・テレオペ", "事務関連派遣職", "秘書", "受付（レセプション）", "学校事務", "その他事務", 
            "企画", "広報・宣伝・販売促進・マーケティング", "派遣コーディネーター", "その他総務・企画", 
            "塾講師", "家庭教師", "試験監督", "その他教育・人材関連", 
            "ドライバー助手", "ドライバー・運転手", "セールスドライバー", "牛乳配達・新聞配達", "バイク便", "大型ドライバー（トラック・バス・牽引）", "配達・配送", "引越し", "フォークリフト", "その他物流/配送", 
            "倉庫・検品", "在庫管理・商品管理", "仕分け", "品出し・ピッキング", 
            "土木工事関連", "設備工事関連", "仕上工事関連", "躯体工事関連", "測量技士", "ＣＡＤオペレーター", "建築・土木現場監督", "建築・設計関連技術者", "設備施工管理・現場監督", "電気・機械設計関連技術者", "組立・加工", 
            "生産管理", "製造業", "機械・電気関連製造", "金属・非鉄金属関連製造", "自動車・輸送用機械製造", 
            "ＳＥ（システムエンジニア）", "プログラマー", "データ入力・PC入力", "ユーザーサポート", "OA・パソコンインストラクター", "IT系派遣職", "ゲームテスター・デバッガー", "その他コンピュータ関連職", 
            "看護師・准看護師", "介護福祉士", "ホームヘルパー（訪問介護等）", "ケアマネージャー", "その他介護スタッフ", "医療事務", "歯科衛生士・歯科技工士", "歯科助手", "マッサージ・セラピスト", "薬剤師", "栄養士・管理栄養士", "医療技術者関連", "看護助手", "理学療法士・作業療法士・言語聴覚士", "保健師", "生活相談員", "介護助手", "保育士・幼稚園教諭", "保育補助", "その他医療", 
            "印刷・製本", "カメラマン（男女）", "広告", "校正", "ビデオ・ラジオ・テレビ局", "その他マスコミ/出版", 
            "モデル・俳優・エキストラ", "キャンペーンスタッフ・キャンペーンガール", "イベントコンパニオン", "その他芸能", 
            "フロアレディ", "カウンターレディ", "ホールスタッフ(ガールズバー・キャバクラ・パブ・クラブ)", "バニーガール", "ママ・チーママ", "店長・マネージャー候補(ガールズバー・キャバクラ・パブ・クラブ)", "店長・マネージャー(ガールズバー・キャバクラ・パブ・クラブ)", 
            "クリエイター", "WEBデザイナー", "デザイナー・イラストレーター", "グラフィックデザイナー", "インテリアコーディネーター", "ＤＴＰオペレーター", "編集・記者・ライター", "美容(エステ・ネイル)", "美容師", "理容師", "ヘアメイク・メイクアップ", "トリマー", "農業・林業・漁業", "造園・庭師", "研究開発技術者", "市場調査", "アンケート・モニター", "通訳・翻訳", "自動車整備士", "メカニック・整備士", "フランチャイズ", "その他派遣職", "その他美容関連", "その他専門職"]
    ] = Field(None, description='職種細分類')
    preferences: List[Literal["短期", "単発・1日OK", "長期歓迎", "春・夏・冬休み期間限定", "時間や曜日が選べる・シフト自由", "土日祝のみOK", "平日のみOK", "週1日からOK", "週2、3日からOK", "週4日以上OK", "時間固定シフト制", "シフト制", "早朝・朝の仕事", "昼からの仕事", "夕方からの仕事", "夜からの仕事", "深夜・夜勤の仕事", "短時間勤務(1日4h以内)", "フルタイム歓迎", "日払い", "週払い", "高収入・高額", "ボーナス・賞与あり", "給与前払いOK", "交通費支給", "まかない・食事補助あり", "社割あり", "研修あり", "資格取得支援制度", "残業なし", "社員登用あり", "送迎あり", "託児所あり", "寮・社宅・住宅手当あり", "産休・育休制度実績あり", "長期休暇あり", "無期雇用派遣", "無期雇用契約", "転勤・店舗異動なし", "職種変更なし", "高校生応援", "大学生歓迎", "未経験・初心者OK", "経験者・有資格者歓迎", "主婦・主夫歓迎", "扶養内勤務OK", "副業・WワークOK", "ブランクOK", "フリーター歓迎", "学歴不問", "ミドル活躍中", "シニア応援", "留学生歓迎", "オープニングスタッフ", "駅チカ・駅ナカ", "バイク通勤OK", "車通勤OK", "リゾート", "英語が活かせる", "在宅ワーク", "髪型・髪色自由", "服装自由", "髭・ネイル・ピアスOK", "制服あり", "履歴書不要", "入社祝い金支給", "即日勤務OK", "友達と応募OK"]
        ] = Field(None)
    
    @root_validator
    def valid_coordinates(cls, v):
        try:
            if not "lng" in v["origins"].keys() and not "lat" in v["origins"].keys():
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Invalid value 'origins'.")
            lng, lat = v["origins"]["lng"], v["origins"]["lat"]
            if not -180.0 <= lng <= 180 or not -90.0 <= lat <= 90:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Invalid value 'origins'. lng({lng}) and lat({lat}) must be in -180<=lng<=180, -90<=lat<=90 respectively.")
            v["origins"] = Point((lng, lat))
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=(e))
        return v

    # @root_validator
    # def radius_commute(cls, v):
    #     if all(v.values()) or not any(v.values()):
    #         raise ValueError('Either radius or commute is required and not both.')
        
    class Config:
        schema_extra = {
            "examples": [
                {
                    "origins": {
                        "type": "Point",
                        "coordinates": [
                            138.4331,
                            34.9635
                        ]
                    },
                    "commute": {
                        "travelMode": "WALKING",
                        "time": "30分"
                    },
                    "jc": [
                        "飲食/フード"
                    ],
                }
            ]
        }
    def str_to_int(self):
        # self.radius = int(self.radius.replace('km', '000').replace('m', '00'))
        self.commute.time = int(self.commute.time.replace('分', ''))
        
