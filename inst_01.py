# -*- coding: utf-8 -*-
# 高阶真实世界实例（工业 / 科研大科学 / 医疗 / 基础设施 / 能源 / 航天）
# 每个条目形如 (类别, 专有名称, 说明正文, 来源URL)

ADVANCED = {
    "microwave": [
        ("科研装置", "法国 ITER 电子回旋共振加热系统", "法国 ITER 聚变装置的电子回旋共振加热（ECRH）系统位于圣保罗莱迪朗斯，由 24 支 170 GHz 回旋管构成，单管输出 1 MW、总功率 20 MW，支持长达 1000 s 的脉冲。装置于 2025 年首次等离子体后逐步投运。其原理是用毫米波在电子回旋频率处与电子共振沉积功率，补偿辐射与热导损失并驱动等离子体电流。", "https://www.iter.org/fr/node/16222"),
        ("科研装置", "中国合肥 EAST 托卡马克 ECRH", "中国合肥中科院等离子体所的 EAST 托卡马克采用电子回旋共振加热，一期为 4 支 140 GHz、单管 1 MW 回旋管，已实现 3.2 MW、100–1000 s 加热；二期扩展至 4.5 MW（140/105 GHz）。微波在等离子体电子回旋层精确沉积能量，用于中心加热与电流驱动，助力长脉冲高约束运行。", "https://inis.iaea.org/records/z92jm-cmp75"),
        ("科研装置", "德国 Wendelstein 7-X 仿星器 ECRH", "德国格赖夫斯瓦尔德的 Wendelstein 7-X 仿星器以 10 MW 连续波 ECRH 运行，由 10 支 1 MW、140 GHz 回旋管提供，是世界上最强的稳态电子回旋加热装置之一。微波经准光反射镜聚焦入真空室，直接加热电子并控制剖面，用于验证仿星器稳态聚变可行性。", "https://www.osti.gov/etdeweb/biblio/20625770"),
        ("科研装置", "中国东莞 CSNS 324 MHz 速调管射频源", "中国东莞的中国散裂中子源（CSNS）以 324 MHz 速调管作为射频功率源，峰值功率 2.5 MW、重复频率 25 Hz，将质子加速至 1.6 GeV，2026 年束流功率达 185 kW（目标 500 kW）。射频腔中的微波电场对质子束团加速，是散裂靶产生中子的基础。", "https://www.newsgd.com/node_5c070fdd03/eb71311503.shtml"),
        ("工业", "美国 CEM MARS 6 微波消解仪", "美国 CEM 公司的 MARS 6「微波消解仪」工作于 2450 MHz，输出 1800 W（整机 3150 W），66 L 腔体，用于土壤、食品、生物样品的酸消解以制备 ICP 分析试样。微波穿透样品使极性分子摩擦生热，在密闭罐内快速升至 200℃ 以上，显著缩短前处理时间。", "https://pdf.directindustry.fr/pdf-en/cem-corporation/mars-6/99459-654015.html"),
        ("工业", "法国 SAIREM 工业微波回温线", "法国 SAIREM 与 IMS 的工业微波回温线工作于 915 MHz，功率 75–300 kW，吞吐 3–12 t/h（MIP-12 达 7700 kg/h），用于冷冻肉、酱料的连续解冻回温。915 MHz 比 2.45 GHz 穿透更深、体积加热更均匀，体积功率密度低、温升平缓，避免表面过热。", "https://www.sairem.com/"),
        ("医疗", "医用微波消融治疗仪", "医用「微波消融治疗仪」（如 FDA 批准的 M150E）以 2450 MHz 发生器输出 0–100 W，经天线针插入肿瘤组织消融。微波使组织内极性分子高速振荡摩擦产热，局部升至 60℃ 以上使蛋白质凝固坏死，针杆以循环水冷却保持 <45℃，用于肝、甲状腺等实体瘤微创治疗。", "https://www.accessdata.fda.gov/cdrh_docs/pdf18/K183153.pdf"),
    ],
    "induction-stove": [
        ("工业", "中国潍坊 CONDUCT 钢壳感应熔炼炉", "中国山东潍坊康达（CONDUCT）电炉的钢壳中频感应熔炼炉，容量覆盖 0.5–60 t，额定功率 400 kW–45 MW，电源频率 50/60 Hz，炉内钢水温度可达 1650℃。感应线圈通入中频电流产生交变磁场，在炉料中感应出涡流直接发热熔化，年供应能力 ≥200 套，服役于铸造与回收冶炼厂。", "https://www.conductfurnace.com/product-energy-saving-steel-shell-induction-melting-furnace.html"),
        ("工业", "中国洛阳鸿腾 10 t 中频感应熔炼炉", "中国河南洛阳鸿腾的 10 t 中频感应熔炼炉额定 7000 kW、频率 300 Hz，钢/铁熔化温度 1515℃，单炉 40–60 分钟，成套已出口东南亚、中东、非洲。电磁感应使金属自身发热，较燃料炉热效率更高、成分更可控，适用于铸钢与合金冶炼。", "https://lyhtdq.en.made-in-china.com/product/ogrpYWVDsxhH/China-10-Ton-Ultra-High-Power-Medium-Frequency-Induction-Steel-Melting-Furnace-Fume-Extraction-System-for-Steel-Mill-Smelting-Plant.html"),
        ("科研装置", "俄罗斯列别杰夫所冷坩埚壳熔法", "俄罗斯莫斯科列别杰夫物理研究所于 1972 年以高频感应加热的冷坩埚「壳熔法」获专利：水冷分瓣铜坩埚中，高频磁场使物料感应发热、内壁凝成冷壳隔绝污染，温度可超 3000℃。该方法用于立方氧化锆晶体生长与核废料玻璃固化，是高温反应材料研究的经典手段。", "https://www.azom.com/article.aspx?ArticleID=20319"),
        ("科研装置", "中国铁岭大型壳熔法设备", "中国辽宁铁岭高频设备厂研制的大型壳熔法设备功率 400–600 kW、频率 800 kHz–1 MHz，冷坩埚直径达 1 m，单炉装料 1 t 以上，成品率约 45%。高频感应使氧化锆粉末在自身冷壳内熔融而不沾污坩埚，用于人造宝石与特种晶体研究生产。", "https://www.jewellery.org.cn/jewelleryorgwebsite/sub/public_link?label_id=381&page_no=1&element_id=3266&element_type=0"),
        ("工业", "北美 Electroheat 钢壳感应熔炼炉", "北美 Electroheat Induction 的钢壳感应熔炼炉输出 50 kW–10 MW，容量 50 kg–20 t，采用 IGBT 中频电源与 PLC/SCADA 控制。交变磁场在金属内感生涡流发热，无需燃烧，热响应快、温度可控，用于钢、铁、铜、铝的铸造与回收熔炼。", "https://electroheatinduction.com/induction-furnace-for-steel-melting"),
        ("工业", "中国江苏宇润 IGBT 中频感应熔炼炉", "中国江苏宇润（YuRun）的 IGBT 中频感应熔炼炉功率 100 kW–3000 kW、容量 50 kg–10 t，较可控硅炉节能 10–20%，已服务 800+ 客户、40+ 国家。电磁感应直接加热炉料，熔化电耗约 490–580 kWh/t，用于钢、铁、铜、铝及特种合金熔炼。", "http://yrmfpower.com/"),
        ("工业", "加拿大 AMELT 钢架感应熔炼炉", "加拿大 Toronto 的 AMELT 钢架感应熔炼炉容量 1–40 t、功率 250 kW–12 MW，熔化速率 1–25 t/h。中频感应涡流使金属内部发热，取代冲天炉熔铸铁，粉尘与排放更低，适用于钢铁与有色金属铸造车间的大批量熔炼。", "https://www.amelt.com/steelframe"),
    ],
    "pressure-cooker": [
        ("工业", "中国 LUY 工业复合/食品蒸压釜", "中国 LUY 机械的工业复合/食品灭菌蒸压釜，直径 600–5000 mm、有效长 1–15 m，工作压力 0.5–5 MPa、温度 100–450℃，年供应能力 5000 套。密封容器内以蒸汽加压提高水的沸点，使食品灭菌或复合材料在均匀温压下固化，已通过 ISO 与 CE-PED 认证。", "https://www.woodtreatmentplant.com/sale-53139127-sports-field-high-temperature-and-pressure-resistant-material-composite-autoclave.html"),
        ("航天与卫星", "中国航空工业 φ7 m×30 m 大型热压罐", "中国航空工业复合材料有限责任公司的 φ7 m×30 m 大型热压罐，可整体成型 30 m 长复合材料构件，用于飞机机翼、机身等主承力结构。罐内以 0.5–2.5 MPa 压缩空气（或惰性气体）与 120–180℃ 对真空袋预浸料加压升温固化，纤维体积分数达 55%–65%。", "https://www.aibangfrp.com/a/8581"),
        ("工业", "Olymspan 航空级复合热压罐", "Olymspan 的航空级全自动复合热压罐工作温度 150℃、压力 1.3 MPa、规格 φ3.5 m×18 m，压力控制精度 ±0.1 MPa，符合 ASME 与 NADCAP。在密封罐内以热空气均匀传热并加压，抑制树脂孔隙、提升碳纤维层合板致密性，用于航空航天与汽车复材。", "https://ar.htnxt.com/page/Composite-Autoclave-Systems:-Core-Technology-and-Industrial-Applications-Guide.html"),
        ("航天与卫星", "德国 SCHOLZ 大型热压罐", "德国 SCHOLZ 公司近四十年来向空客、波音及中航工业（哈飞、西飞、成飞等）交付超 500 台热压罐，在中国已投运 70+ 台，最大规格 φ9 m×60 m。蒸压罐以 100–250℃、最高约 10 MPa 使树脂在真空袋内交联固化，是大型复材构件制造的核心装备。", "https://www.aibangfrp.com/a/8581"),
        ("科研装置", "意大利 Terruzzi 热压罐", "意大利 Terruzzi 向欧洲阿丽亚娜火箭、空客 A380/A320/A400M 提供 600+ 套热压罐，最大 φ9 m×60 m，采用无齿三环罐门与多层加热管。密封容器内对预浸料抽真空并通入压缩空气加压加热，使环氧/聚酰亚胺基体流动交联，制造轻质高强航空结构件。", "https://www.aibangfrp.com/a/8581"),
        ("医疗", "医用高压灭菌器", "医用「高压灭菌器」（autoclave）在 121℃、0.1 MPa（约 15 psi）下维持 20–30 分钟，以饱和蒸汽杀灭器械上的细菌与芽孢。密闭耐压容器内饱和蒸汽压随温度升高而增大，其潜热穿透物品，是医院与实验室器械灭菌的标准手段。", ""),
        ("工业", "中国 SINOMAC 超高温高压热压罐", "中国 SINOMAC 的超高温高压热压罐工作温度 320–380℃、压力 1.5–5 MPa，以氮气氛固化聚酰亚胺等耐高温树脂基复材。密封罐内对真空袋预浸料同步加温加压，用于新一代民机机身筒段、火箭整流罩与卫星结构等战略领域大尺寸构件共固化。", "http://en.czsinomac.com/list_11.html"),
        ("工业", "食品工业高压杀菌釜", "食品工业高压杀菌釜在 115–135℃、0.07–0.3 MPa 下对罐头与软包装灭菌，将中心温度升至 121℃ 并保持数十分钟，灭活肉毒杆菌等耐热菌。密闭容器内饱和蒸汽压高于常压使沸点升高，从而在不破坏包装的前提下延长货架期。", "https://www.endlesswiki.com/wiki/autoclave-processing"),
    ],
    "thermos": [
        ("能源", "中国海油 CGTank 27 万 m³ LNG 储罐", "中国海油 CGTank 超大型 LNG 全容储罐单罐容积 27 万 m³（约 6 个标准泳池），截至 2025 年 11 月已建成 18 座，占全球同型储罐近七成，掌握 3–27 万 m³ 全容技术。双壁结构间抽真空并填保温材料，将 -162℃ 液化天然气日蒸发率压至极低，保障能源储备安全。", "http://www.sasac.gov.cn/n2588025/n2588124/c35053911/content.html"),
        ("能源", "中国石化天津 LNG 接收站", "中国石化天津 LNG 接收站位于天津南港，一、二期共 5 座 22 万 m³ 储罐（二期 2023 年投产），三期规划再建 5 座 27 万 m³ 罐，接卸能力 3 mtpa。储罐为双壁全容、夹层真空绝热，外罐抵御泄漏与火灾，内罐存 -162℃ LNG，是华北天然气调峰枢纽。", "https://www.gem.wiki/Tianjin_LNG_Terminal_%28Sinopec%29"),
        ("科研装置", "CERN LHC 超流氦低温系统", "欧洲核子研究中心（CERN）的大型强子对撞机（LHC）以 1.9 K 超流氦冷却，总冷质量 36,000 t、充注 96 t 氦，制冷功率 144 kW@4.5 K 加 20 kW@1.8 K，隧道长 27 km。超导磁体浸泡于真空夹层「杜瓦」内的超流氦中，利用其极高导热维持 8.33 T 磁场所需低温。", "https://cern-courier.web.cern.ch/a/how-cern-keeps-its-cool/"),
        ("医疗", "医用 MRI 超导磁体液氦杜瓦", "医用 MRI 超导磁体以 4.2 K 液氦浸泡铌钛线圈维持超导，磁场 1.5–3 T，杜瓦为双壁真空夹层、静态蒸发率 <0.1 L/h。真空与多层绝热阻断热传导，使液氦长时间不沸腾，保障磁共振成像所需的稳定强磁场与低运行成本。", ""),
        ("工业", "中国无锡 Triumph 真空绝热低温储罐", "中国无锡 Triumph 的真空绝热低温液体储罐容量 5–200 m³、工作压力 0.8–1.6 MPa、耐 -196℃，双壁真空夹套配多层绝热，日蒸发率（BOR）≤0.05%。用于 LNG、液氮、液氦等低温液体储运，真空层阻断对流与传导，使深冷液体长时间稳定保存。", "http://www.cryotriumph.com/Cryogenic-Liquid-Storage-Tank-pd581291158.html"),
        ("工业", "食品生物冷链真空绝热储罐", "食品与生物制品冷链用真空绝热不锈钢储罐容量 0.5–10 m³，真空夹层可耐 -196～150℃，日蒸发 <0.3%。夹层抽真空并置多层反射屏，大幅降低漏热，用于冰淇淋基料、疫苗与生物样本的中短途低温储运，是移动冷链的关键节点。", "https://gasequipment.ltd/product/lng-cryogenic-storage-tanks-high-capacity-fast-delivery"),
        ("基础设施", "低温液体公路罐车", "低温液体公路罐车采用杜瓦型真空绝热结构，容积 20–50 m³，内胆与外罐间高真空多层绝热，BOR 低。运输 LNG、液氧、液氮时，真空夹层阻断环境传热，使 -196℃ 深冷液体在长途配送中蒸发损失极小，支撑工业气体与清洁能源物流。", "https://gasequipment.ltd/product/lng-cryogenic-storage-tanks-high-capacity-fast-delivery"),
        ("航天与卫星", "航天低温载荷液氦/液氮杜瓦", "航天低温载荷（如空间红外望远镜与探测器）以液氦/液氮杜瓦制冷，工作温区 4.2–80 K，杜瓦采用 30–50 层多层绝热与高真空夹层。深冷剂在真空中缓慢蒸发吸热，将探测器降至近红外本底噪声所需低温，是空间天文与遥感载荷的关键热控部件。", ""),
    ],
    "fridge": [
        ("基础设施", "中国北京麦德龙立水桥跨临界 CO2 制冷", "中国北京麦德龙立水桥店 2018 年投用国内首套跨临界 CO2 制冷系统，销售区约 4100 m²、制冷量 497 kW、供 112 台陈列柜。CO2 在超临界下循环，气体冷却器替代冷凝器，自然工质 GWP=1，较传统制冷剂大幅降低温室效应与泄漏风险。", "http://www.carel.in/story-detail/-/asset_publisher/mFz9iSHGzBlI/content/first-metro-transcritical-co2-store-in-china-efficiency-and-reliability-with-carel-retail-sistema/10191"),
        ("基础设施", "中国张北阿里云浸没式液冷数据中心", "中国河北张北的阿里云数据中心部署浸没式液冷集群，服务器规模 38 万+，将主板浸于绝缘冷却液中，热量由液体直接带走进入外循环，节能 >70%，年均 PUE 最低 1.09。张北年均 2.6℃ 的冷凉气候配合液冷，实现几乎无机械制冷的绿色散热。", "https://baike.baidu.com/item/%E9%98%BF%E9%87%8C%E5%B7%B4%E5%B7%B4%E4%BF%A1%E6%81%AF%E7%A7%91%E6%8A%80%EF%BC%88%E5%BC%A0%E5%8C%97%EF%BC%89%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/20619298"),
        ("科研装置", "CERN LHC 低温制冷厂", "CERN 大型强子对撞机的低温制冷厂由 8 个低温岛组成，提供 144 kW@4.5 K 与 20 kW@1.8 K 制冷功率，总电输入 32 MW，维持 27 km 隧道内 1.9 K 超流氦。多级涡轮膨胀与液氮预冷将氦气逐级液化，是迄今最大的液氦温区制冷系统。", "https://cern-courier.web.cern.ch/a/the-challenge-of-keeping-cool"),
        ("工业", "中国理化所/齐耀动力 LNG 船 BOG 再液化", "中科院理化所联合上海齐耀动力研制的 LNG 船用混合工质型 BOG 再液化装置，形成 0.5–1.5 t/h 系列；1 t/h 样机通过中国船级社认证，1.5 t/h 装置通过沪东中华验收、2025 年交付。低温制冷机将蒸发气重新液化回液货舱，避免排放并稳定舱压。", "https://cryo.ipc.cas.cn/xwdt/kydt/202504/t20250409_530585.html"),
        ("工业", "中国成都 TCWY BOG 再液化装置", "中国四川成都 TCWY 的 BOG 再液化装置处理能力 30–500 t/天，单位能耗 500–800 kW·h/t，液氮法另耗 2 t LIN/t。采用逆布雷顿氮循环或液氮冷却，将 LNG 蒸发气重新液化，用于接收站与运输船的零排放保冷物流。", "https://www.maoyt.com/test/tcwygasplant.com/sale-11309779-boil-off-gas-bog-lng-reliquefaction-plant-with-30-to-500-tons-per-day-capacity.html"),
        ("能源", "荷兰 Staay 全球最大 CO2 制冷系统", "荷兰 Dronten 的 Staay Food Group 拥有全球最大 CO2 制冷系统，总容量 3.36 MW，服务于蔬菜加工与城市农业大棚的温湿度调控，年产能 30 万 kg 生菜。跨临界 CO2 在增压循环中既制冷又回收废热，是大型食品冷链的能效标杆。", "https://www.mdpi.com/1996-1073/12/15/2959/xml"),
        ("工业", "欧洲商超跨临界 CO2 制冷系统", "欧洲商超已投运超 40,000 套跨临界 CO2 制冷系统，单店制冷负荷 150–600 kW，北美部署超 3500 套。CO2 增压系统以跨临界循环取代 HFC，制冷剂年泄漏率 <10%，并可通过热回收满足约 65% 门店供暖需求，是零售业低碳制冷主流方案。", "https://www.precisionreports.co/market-reports/transcritical-co2-refrigeration-unit-market-600197"),
        ("科研装置", "稀释制冷机低温系统", "「稀释制冷机」是超导量子计算与凝聚态研究的核心制冷装置，基准温度可低至 10 mK，先由脉冲管/GM 制冷预冷至 4 K，再经 3He/4He 混合室稀释降温。多级真空绝热与换热将微观系统逼近绝对零度，使量子比特与低温物性实验得以进行。", ""),
    ],
}
