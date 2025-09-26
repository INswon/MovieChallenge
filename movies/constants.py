# 映画推薦で選択できる感情
RECOMMEND_CATEGORY = {
    "healing":     {"label": "癒された", "order": 1},
    "impression":  {"label": "泣いた", "order": 2},
    "energy":      {"label": "興奮した","order": 3},
    "scary":       {"label": "怖かった","order": 4},
    "curious":     {"label": "新鮮だった","order": 5}
}

# おすすめ表示映画作品
RECOMMEND_MOVIE = {
    "healing": [
        {
            "title": "最強のふたり",
            "overview": "実話に基づく感動作。友情が心をあたたかくする",
            "genres": ["ドラマ","コメディ"],
            "rating": 4.2
        },
        {
            "title": "かもめ食堂",
            "overview": "フィンランドで営む小さな食堂。穏やかで優しい時間",
            "genres": ["ドラマ","コメディ"],
            "rating": 3.9
        },
        {
            "title": "スモーク",
            "overview": "街角のタバコ屋と人々の交流。静かで心地よい余韻",
            "genres": ["ドラマ"],
            "rating": 4.0
        }
    ],
    "impression": [
        {
            "title": "タイタニック",
            "overview": "運命に翻弄されるラブストーリー。涙なしでは見られない不朽の名作",
            "genres": ["ドラマ","恋愛","パニック"],
            "rating": 4.0
        },
        {
            "title": "私の頭の中の消しゴム",
            "overview": "愛する人が記憶を失っていく切なさ。純粋な愛の尊さに心を打たれる",
            "genres": ["ドラマ","恋愛"],
            "rating": 3.9
        },
        {
            "title": "ラ・ラ・ランド",
            "overview": "夢を追う二人の恋と別れ。美しい音楽と映像で胸が熱くなる",
            "genres": ["恋愛","ミュージカル"],
            "rating": 3.9
        }
    ],
    "energy": [
        {
            "title": "ベイビー・ドライバー",
            "overview": "音楽×カーチェイスの多幸感。テンポ良く一気見",
            "genres": ["音楽", "アクション"],
            "rating": 4.0
        },
        {
            "title": "キングスマン",
            "overview": "キレキレのスパイ・アクション。“気絶モード”の快感",
            "genres": ["アクション"],
            "rating": 4.1
        },
        {
            "title": "アンチャーテッド",
            "overview": "財宝を追う冒険活劇。王道アドベンチャーでワクワク",
            "genres": ["アクション","アドベンチャー","冒険"],
            "rating": 3.7
        }
    ],
    "scary": [
        {
            "title": "羊たちの沈黙",
            "overview": "心理戦と異常犯罪の緊迫感。静かな恐怖が背筋を凍らせる",
            "genres": ["クライム","サスペンス"],
            "rating": 4.0
        },
        {
            "title": "ザ・メニュー",
            "overview": "美食の場で展開する狂気のサスペンス。予測不能の展開に不安が募る",
            "genres": ["ホラー"],
            "rating": 3.6
        },
        {
            "title": "エクソシスト",
            "overview": "悪魔に憑かれた少女を巡る衝撃の恐怖体験。ホラー映画の金字塔",
            "genres": ["ホラー"],
            "rating": 3.3
        }
    ],
    "curious": [
        {
            "title": "インセプション",
            "overview": "夢の中の夢を舞台にした頭脳ゲーム。複雑で新鮮な設定に引き込まれる",
            "genres": ["SF","アクション","アドベンチャー","サスペンス","冒険"],
            "rating": 4.1
        },
        {
            "title": "インターステラー",
            "overview": "科学と愛をテーマにした壮大な宇宙探査。知的好奇心を刺激する傑作",
            "genres": ["ドラマ","アドベンチャー","冒険","SF"],
            "rating": 4.2
        },
        {
            "title": "メメント",
            "overview": "記憶を失う主人公の物語が逆再生される構成。意外性と深い考察を誘う",
            "genres": ["サスペンス","ミステリー","スリラー"],
            "rating": 3.9
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
