# 映画推薦で選択できる感情
RECOMMEND_CATEGORY = {
    "healing":     {"label": "癒された", "order": 1},
    "impression":  {"label": "泣いた", "order": 2},
    "energy":      {"label": "興奮した","order": 3},
    "scary":       {"label": "怖かった","order": 4},
    "curious":     {"label": "新鮮だった","order": 5},
}

# おすすめ表示映画作品
RECOMMEND_MOVIE = {
    "healing": [
        {
            "title": "最強のふたり",
            "note": "実話に基づく感動作。友情が心をあたたかくする",
            "poster": "",
            "year": 2011,
        },
        {
            "title": "かもめ食堂",
            "note": "フィンランドで営む小さな食堂。穏やかで優しい時間",
            "poster": "",
            "year": 2006,
        },
        {
            "title": "スモーク",
            "note": "街角のタバコ屋と人々の交流。静かで心地よい余韻",
            "poster": "",
            "year": 1995,
        }
    ],
    "impression": [
        {
            "title": "タイタニック",
            "note": "運命に翻弄されるラブストーリー。涙なしでは見られない不朽の名作",
            "poster": "",
            "year": 1997,
        },
        {
            "title": "私の頭の中の消しゴム",
            "note": "愛する人が記憶を失っていく切なさ。純粋な愛の尊さに心を打たれる",
            "poster": "",
            "year": 2004,
        },
        {
            "title": "ラ・ラ・ランド",
            "note": "夢を追う二人の恋と別れ。美しい音楽と映像で胸が熱くなる",
            "poster": "",
            "year": 2016,
        }
    ],
    "energy": [
        {
            "title": "ベイビー・ドライバー",
            "note": "音楽×カーチェイスの多幸感。テンポ良く一気見",
            "poster": "",  
            "year": 2017,
        },
        {
            "title": "キングスマン",
            "note": "キレキレのスパイ・アクション。“気絶モード”の快感",
            "poster": "",
            "year": 2015,
        },
        {
            "title": "アンチャーテッド",
            "note": "財宝を追う冒険活劇。王道アドベンチャーでワクワク",
            "poster": "",
            "year": 2022,
        }
    ]
}

MOOD_CATEGORY_MAP = {
    # healing（癒し・落ち着き）
    "癒された": "healing",
    "優しかった": "healing",
    "ほのぼのした": "healing",
    "安心した": "healing",
    "あたたかい気持ちになった": "healing",
    "落ち着いた": "healing",
    "穏やかだった": "healing",
    "心地よかった": "healing",
    
    # impression（感動・涙）
    "涙": "impression",
    "泣いた": "impression",
    "感動": "impression",
    "共感した": "impression",
    "胸が熱くなった": "impression",
    "切なかった": "impression",
    "ジーンときた": "impression",
    "胸が苦しくなった": "impression",
    "涙が止まらなかった": "impression",

    # energy（興奮・楽しい) , 映画ジャンル(アクション,SF, スポーツ映画)
    "興奮": "energy",
    "笑った": "energy",
    "テンション上がった": "energy",
    "爽快だった": "energy",
    "元気が出た": "energy",
    "ワクワクした": "energy",
    "盛り上がった": "energy",
    "楽しかった": "energy",
    "熱くなった": "energy",

    # scary（緊張・ホラー）, 映画ジャンル(ホラー系統)
    "怖い": "scary",
    "緊張した": "scary",
    "ゾクッとした": "scary",
    "不安になった": "scary",
    "ハラハラした": "scary",
    "息が詰まった": "scary",
    "衝撃を受けた": "scary",
    "心臓がドキドキした": "scary",

    # curious（好奇心・新鮮さ）
    "新鮮": "curious",
    "新鮮だった": "curious",
    "考えさせられた": "curious",
    "興味深かった": "curious",
    "驚いた": "curious",
    "知的だった": "curious",
    "学びがあった": "curious",
    "展開が読めなかった": "curious",
    "視点が面白かった": "curious",
    "意外性": "curious"
}

MOOD_HERO_IMAGES = {
    "energy": "images/hero/excitement.jpg",
    "healing": "images/hero/healing.jpg",
    "impression": "images/hero/impression.jpg",
    "scary": "images/hero/scary.jpg",
    "curious": "images/hero/curious.jpg",
    "default": "images/hero/default.jpg",
}
