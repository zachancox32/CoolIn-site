# -*- coding: utf-8 -*-
"""Content for the commercial sector pages.

Each of these sectors used to be one H3 inside a card grid on commercial.html.
Six different search markets with six different buyers were sharing a single
page, so at best one of them could rank. They are separate pages now, each
written against how that kind of building actually behaves rather than
templated from the others.

Nothing here is boilerplate: the prose, the prices and the FAQs differ per
sector on purpose, because thin near duplicate pages are worse than no pages.
"""

SECTORS = [

# ---------------------------------------------------------------- offices
{
 'slug': 'office-air-conditioning',
 'crumb': 'Offices',
 'eyebrow': 'Offices and workspaces',
 'h1a': 'Office air conditioning',
 'h1b': 'in Manchester',
 'title': 'Office Air Conditioning Manchester | CoolIn',
 'desc': 'Office air conditioning designed, fitted and serviced across Manchester '
         'and the North West. Cassettes, slim ducted and VRF, zoned room by room.',
 'lede': 'A floor plate with a glass south wall and a cold north corner needs '
         'zoning, not a bigger unit. We survey how the space is actually used '
         'through the working day, size against the real heat load, and fit in '
         'the evenings so nobody loses a desk.',
 'trust': [('Zoned control', 'room by room, not floor by floor'),
           ('Evenings', 'fitted outside office hours'),
           ('From £2,450', 'one cassette, installed')],
 'kf_lead': 'CoolIn designs, installs and maintains office air conditioning across '
            'Manchester city centre and the wider North West, from a single meeting '
            'room to a multi floor VRF system. Most office work is done outside '
            'trading hours at standard labour rates, so the floor is usable the '
            'next morning.',
 'kf': [('Typical systems', 'Ceiling cassettes, slim ducted, VRF'),
        ('One room', 'From £2,450 installed'),
        ('Open plan floor', 'Around £8,500 for four cassettes'),
        ('Fitting hours', 'Evenings and weekends, standard rates'),
        ('Compliance', 'TM44 over 12kW, F-Gas over 5 tonnes CO2e'),
        ('Servicing', 'From £89 per indoor unit per year')],
 'ch_eyebrow': 'What makes offices difficult',
 'ch_h2': 'Why an office is harder to cool than the floor area suggests',
 'ch_sub': 'Nearly every office we are called back to was sized off a square metre '
           'rule of thumb. Four things break that rule, and all four are visible '
           'on a survey if anyone bothers to look.',
 'challenges': [
   ('The glass side and the cold side',
    'A south or west facing elevation can take a room several degrees above the one '
    'behind it on the same floor, and the gap moves through the day. One system '
    'set to one temperature will always be cooling one half and overcooling the '
    'other. The fix is zoning at design stage, not a compromise setpoint later.',
    'Solar gain modelled per elevation'),
   ('The meeting room that fills at two o\'clock',
    'A person sitting at a desk gives off roughly the heat of a small light bulb, '
    'and a room of twelve in a glass box with the door shut climbs fast. Meeting '
    'rooms are the single most common complaint in an office, and they are almost '
    'always undersized because they were counted as floor area rather than as '
    'people.',
    'Sized on occupancy, not square metres'),
   ('Equipment nobody counted',
    'Desktop machines, monitors, a printer, and the comms cupboard that runs a '
    'switch and a firewall every hour of the year. In a small office that stack '
    'can be a meaningful share of the total load, and the comms cupboard often '
    'needs its own <a href="server-room-cooling">dedicated cooling</a> rather than '
    'a share of the open plan system.',
    'Equipment load added to the calculation'),
   ('Everyone has a different opinion',
    'Give a floor one controller and you get a thermostat war. We set zones that '
    'match how people actually sit, lock the range so nobody can drive it to 16 '
    'degrees, and hand over the controls to whoever runs the office rather than '
    'leaving a remote in a drawer.',
    'Locked setpoint ranges as standard')],
 'sy_h2': 'Which system suits your office',
 'sy_sub': 'The ceiling decides most of this. What sits above the tiles, and whether '
           'there is a void at all, narrows the options before anything else does.',
 'systems': [
   ('Ceiling cassette',
    'The default where there is a suspended ceiling. Sits flush in a tile grid, '
    'throws air four ways, and is the cheapest route to even coverage across open '
    'plan. Needs around 300mm of void.'),
   ('Slim ducted',
    'The unit hides in the void and feeds linear grilles, so the ceiling stays '
    'clean. The usual choice on a designed fit out, or where a landlord or a '
    'listed frontage will not accept visible plant.'),
   ('VRF and VRV',
    'One outdoor unit serving many indoor ones, with heat recovery moving heat '
    'from the sunny side to the shaded side rather than dumping it outside. Worth '
    'the extra capital cost from roughly six indoor units upward.'),
   ('Wall mounted split',
    'Cheapest per room and the right answer for a small office, a single meeting '
    'room, or a period building with no ceiling void to work with.')],
 'co_h2': 'What office air conditioning costs',
 'co_sub': 'Installed prices covering equipment, labour, commissioning and handover. '
           'Commercial jobs are priced per project because ceiling voids, riser '
           'routes and access all move the figure, so treat these as budget bands '
           'rather than quotations.',
 'prices': [
   ('Small office', 'Up to about 30 square metres', [
     ('Wall unit, 5kW', '£2,280'),
     ('Single cassette, 3.5kW', '£2,450'),
     ('Meeting room, one unit', 'from £2,450'),
     ('Two rooms, one condenser', '£4,400')]),
   ('Office floor', 'Open plan plus meeting rooms', [
     ('Four cassette system', '£8,500'),
     ('Slim ducted, two zones', '£3,500'),
     ('Six unit VRF', '£14,000'),
     ('Heat recovery ventilation', '£5,200')]),
   ('Multi floor', 'Whole building or phased fit out', [
     ('VRF, whole building', 'per project'),
     ('Comms room close control', 'from £9,000'),
     ('Plant replacement', 'per project'),
     ('Phased floor by floor', 'per project')])],
 'price_note': '<strong>These are guide bands, not quotations.</strong> An office '
               'quote from us shows the heat load calculation for each area with '
               'the working visible, an equipment schedule with positions and '
               'pipework routes, the electrical requirement, and a programme set '
               'around your working hours. The survey costs nothing and the written '
               'price does not move.',
 'du_nav': 'Duties',
 'du_eyebrow': 'Compliance and tenancy',
 'du_h2': 'The duties that come with an office system',
 'du_sub': 'Two of these are law and catch more offices than people expect. The '
           'third is not law at all, and is the one that costs tenants money at '
           'the end of a lease.',
 'duties': [
   ('TM44 inspections',
    ['Any building with air conditioning over 12kW of effective rated output needs '
     'an inspection by an accredited energy assessor at least every five years. '
     'That threshold is far lower than most office managers assume.',
     'Four 3.5kW cassettes on one floor already cross it. So does a single small '
     'VRF. The duty sits with the building owner or whoever controls the system, '
     'not with the company that fitted it, and the report goes on the national '
     'register.'],
    'We flag systems that are over the threshold during servicing, so a renewal '
    'date never arrives as a surprise.'),
   ('F-Gas record keeping',
    ['Systems are measured by the refrigerant they hold converted into tonnes of '
     'CO2 equivalent. Past 5 tonnes, the operator has to arrange leak checks and '
     'keep records. With R32 that line sits at roughly 7.4kg of refrigerant.',
     'A handful of cassettes on separate condensers will usually sit under it. An '
     'office VRF almost always sits over it, and then the duty is annual at '
     'minimum. The full thresholds are set out on the '
     '<a href="commercial#compliance">commercial page</a>.'],
    'Nobody opens a refrigerant circuit on your system without current F-Gas '
    'certification. That is a legal requirement for handling refrigerant, not a '
    'preference.'),
   ('Landlord consent and dilapidations',
    ['Most office leases require written consent before plant is fixed to the '
     'structure or a core is drilled through an external wall, and a serviced '
     'building will often have its own rules about condenser positions and roof '
     'access.',
     'The part tenants miss is the other end. A lease that requires reinstatement '
     'means stripping the system out and making good when you leave, which is a '
     'cost worth pricing before you commit rather than discovering at exit.'],
    'We will put the equipment schedule and condenser positions in writing for a '
    'landlord application, which is normally what gets consent moving.')],
 'faqs': [
   ('Can you install without closing the office?',
    'Yes, and most office work is done this way. We work evenings and weekends at '
    'standard labour rates rather than a premium, sheet and clear the area each '
    'night, and phase larger floors so only one part of the office is affected at '
    'a time. A single meeting room is usually one evening.'),
   ('How much mess does it make to a suspended ceiling?',
    'Cassettes drop into the existing grid, so the tiles come out and go back. '
    'Pipework runs in the void. The visible work is the core through the external '
    'wall for the pipe route and the condenser position outside, and those are the '
    'two things worth agreeing with your landlord before we start.'),
   ('Does every room need its own unit?',
    'No. Open plan is normally covered by several units on shared control, while '
    'meeting rooms and any room with a different aspect get their own zone. The '
    'point of zoning is that the rooms that behave differently are controlled '
    'differently, not that every door gets its own box.'),
   ('What does it cost to run?',
    'A modern inverter system uses around a quarter to a third of the electricity '
    'of an old fixed speed one for the same output, because it modulates rather '
    'than cycling on and off. As a rough figure, a 3.5kW cassette holding a '
    'meeting room on a warm afternoon draws roughly the power of a desktop '
    'computer and a monitor once it has pulled the room down.'),
   ('Do we need a TM44 inspection?',
    'If the installed air conditioning in the building is over 12kW of effective '
    'rated output, yes, at least every five years, with the first within five '
    'years of the system going into service. Four 3.5kW cassettes cross the line. '
    'The duty is the building owner\'s or the operator\'s, not the installer\'s.'),
   ('How long does a full floor take?',
    'A four cassette open plan floor is typically three to five days on site '
    'including commissioning. A VRF system across several floors is programmed '
    'floor by floor and quoted with a written programme, so you know which week '
    'affects which team.')],
 'areas_line': 'We fit office systems across Manchester city centre, Salford Quays, '
               'Spinningfields and the wider North West',
 'service_type': 'Office air conditioning installation',
 'ld_desc': 'Design, installation, servicing and repair of office air conditioning '
            'in Manchester and across the North West, including ceiling cassettes, '
            'slim ducted systems and VRF with zone control.',
},

# ----------------------------------------------------------------- retail
{
 'slug': 'retail-air-conditioning',
 'crumb': 'Shops and salons',
 'eyebrow': 'Retail, salons and showrooms',
 'h1a': 'Shop and retail',
 'h1b': 'air conditioning',
 'title': 'Shop and Retail Air Conditioning Manchester | CoolIn',
 'desc': 'Air conditioning for shops, salons and showrooms across Manchester and the '
         'North West. Sized for a propped open door, and fitted overnight.',
 'lede': 'A shop floor has to stay comfortable with the front door held open all '
         'day, the window full of sun, and lighting running from opening to close. '
         'We size for how retail actually trades, and fit overnight so you never '
         'lose a day\'s takings.',
 'trust': [('Overnight', 'fitted between closing and opening'),
           ('Open door', 'sized for how shops really trade'),
           ('From £2,280', 'one unit, installed')],
 'kf_lead': 'CoolIn installs and maintains air conditioning for shops, hair and '
            'beauty salons, showrooms and small retail units across Manchester and '
            'the North West. Retail work is almost always done between closing and '
            'opening, so the shutters go up on time.',
 'kf': [('Typical systems', 'Cassettes, slim ducted, wall units'),
        ('Small unit', 'From £2,280 installed'),
        ('Salon or larger floor', 'From £4,400 for two units'),
        ('Fitting hours', 'Overnight and Sundays, standard rates'),
        ('Lead time', 'Usually inside two weeks from survey'),
        ('Servicing', 'From £89 per indoor unit per year')],
 'ch_eyebrow': 'What makes retail different',
 'ch_h2': 'Cooling a space that is deliberately open to the street',
 'ch_sub': 'Retail breaks the assumptions every heat load calculation starts from. '
           'A sealed room is easy. A shop with the door wedged open in August is a '
           'different problem, and undersizing here is the most common mistake we '
           'are called in to correct.',
 'challenges': [
   ('The door stays open',
    'Retailers prop the door because a closed door costs footfall, and no amount of '
    'engineering changes that. What it means is a continuous load the calculation '
    'has to allow for rather than pretend away. Sized properly the shop still holds '
    'temperature. Sized as a sealed room it runs flat out and never gets there.',
    'Infiltration allowed for at design'),
   ('A window full of afternoon sun',
    'A glazed shopfront facing the street is a solar collector, and the display '
    'lighting behind it adds more. The front of the shop and the back of the shop '
    'are effectively two different rooms, which is why a single unit in the middle '
    'satisfies nobody.',
    'Front and rear treated separately'),
   ('Nobody wants to stand under it',
    'A customer or a stylist standing directly in the throw will be uncomfortable '
    'within a minute, and in a salon it also disturbs a blow dry. Position matters '
    'as much as capacity: units go over circulation space and away from tills, '
    'chairs and fitting rooms.',
    'Positioned around where people stand'),
   ('Salons have their own load',
    'Dryers, straighteners and backwash units put real heat into a room that also '
    'needs the air changing rather than just chilling, because of product fumes '
    'and humidity. Cooling alone will not fix a salon that smells, so '
    '<a href="ventilation">ventilation</a> usually belongs in the same design.',
    'Cooling and air change designed together')],
 'sy_h2': 'Which system suits a retail space',
 'sy_sub': 'The fit out usually decides it. How much you are willing to see on the '
           'ceiling, and whether there is a void to hide anything in, narrows the '
           'choice quickly.',
 'systems': [
   ('Ceiling cassette',
    'Flush in a tile ceiling with a four way throw, which suits a square shop floor '
    'and keeps the walls clear for stock and mirrors. The usual starting point '
    'where a suspended ceiling exists.'),
   ('Slim ducted with matched grilles',
    'The unit hides in the void and only a linear grille shows, which can be colour '
    'matched to the ceiling. The right answer where the ceiling is part of the '
    'brand, in showrooms and in higher end salons.'),
   ('Wall mounted split',
    'Cheapest per room and quick to fit. Best mounted high on a side wall aimed '
    'across the space rather than down at the till, and the sensible choice for a '
    'small unit or a period building with no void.'),
   ('Extract and make up air',
    'Not cooling at all, and sometimes the actual answer. Salons, nail bars and '
    'barbers frequently need air changed rather than chilled, and a heat recovery '
    'unit does that without throwing the heating bill away.')],
 'co_h2': 'What retail air conditioning costs',
 'co_sub': 'Installed prices covering equipment, labour, commissioning and handover. '
           'Retail jobs vary with access, ceiling height and where the condenser can '
           'physically go, so treat these as budget bands rather than quotations.',
 'prices': [
   ('Small shop or salon', 'One trading space', [
     ('Wall unit, 5kW', '£2,280'),
     ('Single cassette, 3.5kW', '£2,450'),
     ('Slim ducted, one zone', 'from £2,900'),
     ('Extract and make up air', 'from £2,400')]),
   ('Larger unit', 'Front and rear, or two floors', [
     ('Two cassettes, one condenser', '£4,400'),
     ('Slim ducted, two zones', '£3,500'),
     ('Four cassette system', '£8,500'),
     ('Heat recovery ventilation', '£5,200')]),
   ('Showroom or chain', 'Multi site or high ceiling', [
     ('Six unit VRF', '£14,000'),
     ('High level ducted', 'per project'),
     ('Multi site rollout', 'per project'),
     ('Plant replacement', 'per project')])],
 'price_note': '<strong>These are guide bands, not quotations.</strong> The two '
               'things that move a retail price most are the condenser position, '
               'because a rear yard is cheap and a roof with no safe access is not, '
               'and whether the work has to happen overnight. We quote out of hours '
               'labour at standard rates, so trading overnight does not carry a '
               'premium.',
 'du_nav': 'Landlord',
 'du_eyebrow': 'Consent and compliance',
 'du_h2': 'Permission, neighbours and the paperwork',
 'du_sub': 'Retail units come with more people to satisfy than most commercial '
           'spaces. A shopping centre, a landlord and sometimes a planning officer '
           'all have a view on where the outdoor unit goes.',
 'duties': [
   ('Landlord and centre consent',
    ['Almost every retail lease needs written consent before plant is fixed to the '
     'building or a core is drilled through a wall, and a shopping centre will have '
     'its own rules on condenser locations, roof access and working hours.',
     'Getting this moving early is the single biggest cause of delay on retail '
     'jobs. What a landlord normally wants is an equipment schedule, the condenser '
     'position marked up, and the noise rating of the unit.'],
    'We put that pack together as part of the quote, because a survey that ignores '
    'consent just moves the problem.'),
   ('Planning and listed frontages',
    ['An external condenser on a listed building, or one visible from the street in '
     'a conservation area, can need consent in its own right. Manchester has a lot '
     'of both, particularly in the Northern Quarter and around the city core.',
     'Where the front is protected, the work goes to the rear or the roof and the '
     'pipe run gets longer, which is a cost worth knowing at survey rather than at '
     'installation.'],
    'Noise to a neighbouring residential property is the other common objection, '
    'and it is answered with the unit\'s rated sound level and its position.'),
   ('F-Gas and TM44',
    ['A single shop system will normally hold well under 5 tonnes of CO2 equivalent '
     'refrigerant, so no leak check duty applies. Several units across a larger '
     'unit can change that.',
     'TM44 catches more retailers than they expect, because the 12kW threshold is '
     'for the whole building rather than per unit. A parade with one owner can '
     'cross it easily.'],
    'We work out where your system sits against both thresholds at survey and put '
    'it in writing, so it is not left to guesswork.')],
 'faqs': [
   ('Will air conditioning work with the door open?',
    'Yes, provided it was sized knowing the door would be open. The open door is a '
    'continuous heat gain, and a system designed for a sealed room will run '
    'permanently and still lose. We measure the opening and allow for it, which is '
    'why our figure for a shop is usually higher than a domestic room of the same '
    'size. An air curtain over the door reduces it further where it suits the '
    'frontage.'),
   ('Can you fit it without closing the shop?',
    'Yes. Most retail installs are done overnight or on a Sunday, with the floor '
    'sheeted and cleared before opening. We charge standard labour rates for out of '
    'hours work rather than a premium, because for retail it is the normal way to '
    'do the job rather than a special request.'),
   ('Do we need the landlord\'s permission?',
    'Almost certainly, if anything is fixed to the structure or a hole goes through '
    'an external wall. Check the alterations clause in your lease. We supply the '
    'equipment schedule, the condenser position and the noise rating that a '
    'landlord or centre management normally asks for before consenting.'),
   ('Will the outside unit annoy the flat above?',
    'It is the most common objection and it is manageable. Modern condensers have a '
    'published sound power level, night mode settings drop it further, and position '
    'and anti vibration mounts do the rest. We check the nearest sensitive window '
    'at survey rather than after a complaint.'),
   ('Our salon gets hot and smells. Is cooling the answer?',
    'Partly. Cooling deals with the heat from dryers and lighting, but smell and '
    'humidity are an air change problem, and recirculating cooled air does not fix '
    'them. Most salons need both, and a heat recovery unit changes the air without '
    'throwing away the heat you have paid for.'),
   ('How long does a shop installation take?',
    'A single unit is usually one night. Two units on a shared condenser is '
    'typically two. Anything involving ductwork or a roof condenser is quoted with '
    'a written programme so you know exactly which nights are affected.')],
 'areas_line': 'We fit retail systems across Manchester, the Trafford Centre area, '
               'Altrincham, Wilmslow and the wider North West',
 'service_type': 'Retail air conditioning installation',
 'ld_desc': 'Air conditioning installation, servicing and repair for shops, salons '
            'and showrooms in Manchester and across the North West, fitted outside '
            'trading hours.',
},

# ------------------------------------------------------------ hospitality
{
 'slug': 'restaurant-air-conditioning',
 'crumb': 'Restaurants and bars',
 'eyebrow': 'Restaurants, bars and kitchens',
 'h1a': 'Restaurant, bar and kitchen',
 'h1b': 'air conditioning',
 'title': 'Restaurant and Kitchen Air Conditioning Manchester | CoolIn',
 'desc': 'Kitchen extract, make up air and front of house cooling for restaurants '
         'and bars in Manchester and the North West. Gas interlock and DW/172 '
         'ductwork.',
 'lede': 'A canopy pulling hard over the line has to have air coming back in from '
         'somewhere, or the kitchen fights itself and the dining room gets the '
         'smell. We design extract, make up air and front of house cooling as one '
         'system, because that is how the building behaves.',
 'trust': [('Overnight', 'fitted between service and service'),
           ('Gas interlock', 'wired and certificated'),
           ('DW/172', 'kitchen ductwork to specification')],
 'kf_lead': 'CoolIn designs and installs kitchen extract, make up air, front of '
            'house cooling and cellar cooling for restaurants, bars, cafes and pubs '
            'across Manchester and the North West. Hospitality work is programmed '
            'around service, normally overnight or on a closed day.',
 'kf': [('Typical systems', 'Canopy extract, make up air, cassettes, cellar cooling'),
        ('Kitchen extract and make up', 'From £6,500 installed'),
        ('Front of house', 'From £4,400 for two units'),
        ('Ductwork standard', 'DW/172 for kitchen extract'),
        ('Gas safety', 'Interlock required under BS 6173'),
        ('Fitting hours', 'Overnight or closed days, standard rates')],
 'ch_eyebrow': 'What makes kitchens different',
 'ch_h2': 'Why the kitchen is still hot with the extract running',
 'ch_sub': 'This is the call we get most often in hospitality, and it is almost '
           'never the canopy fan. A kitchen is an air balance problem before it is '
           'a cooling problem, and until the balance is right nothing else helps.',
 'challenges': [
   ('Air has to come back in',
    'A canopy can pull a serious volume of air out of a kitchen every hour. If '
    'there is no designed route for replacement air, the extract pulls it through '
    'the only openings available, which is usually the dining room and the back '
    'door. The fan strains, the extract rate drops below what it says on paper, and '
    'the kitchen stays hot.',
    'Make up air designed to match the canopy'),
   ('The dining room ends up smelling of the kitchen',
    'That backwards flow is exactly why. Air that should be leaving through the '
    'canopy travels the wrong way into the front of house instead, taking the '
    'cooking smell with it. Balancing the kitchen fixes the dining room as a side '
    'effect, which surprises operators who assumed they needed more cooling out '
    'front.',
    'Kitchen held slightly negative to front of house'),
   ('Front of house is a separate system',
    'The dining room needs comfort cooling sized for a full house on a hot '
    'Saturday, with people, candles, lighting and a bar all contributing. Trying to '
    'serve it from the same system as the kitchen gives you a dining room that '
    'smells and a kitchen that is never cold enough.',
    'Dedicated cooling for the customer side'),
   ('Bars have a cellar as well',
    'Keg and cask cellars want holding steadily in the low to mid teens, and a '
    'cellar that drifts costs you beer quality and yield before it costs you '
    'anything else. It is a different kind of cooling from the dining room and it '
    'belongs in the design from the start.',
    'Cellar cooling designed with the rest')],
 'sy_h2': 'What a hospitality fit out actually involves',
 'sy_sub': 'Four separate systems in most restaurants, and they have to be designed '
           'together. Quoting one of them in isolation is how operators end up '
           'paying twice.',
 'systems': [
   ('Canopy and extract',
    'The canopy, grease filters and ductwork carrying the extract to a discharge '
    'point that does not upset the neighbours. Kitchen extract ductwork is built to '
    'DW/172, with access panels so it can be cleaned rather than sealed up and '
    'forgotten.'),
   ('Make up air',
    'A supply unit bringing replacement air back into the kitchen, tempered so the '
    'brigade is not standing in a draught of cold outside air in January. This is '
    'the part most often missing from a kitchen that does not work.'),
   ('Front of house cooling',
    'Cassettes or slim ducted units sized for a full room, positioned so nobody is '
    'sitting directly in the throw and the staff side is not left out. Zoned '
    'separately from the bar, which runs warmer.'),
   ('Cellar cooling',
    'A dedicated cellar unit holding the room steady year round, with the condenser '
    'sited where its heat and noise are not a problem. Sized on the cellar volume, '
    'the ground it sits in and the delivery pattern, not on floor area.')],
 'co_h2': 'What a restaurant or bar system costs',
 'co_sub': 'Installed prices covering equipment, labour, commissioning and handover. '
           'Hospitality varies more than any other sector we work in, because the '
           'duct route to a discharge point can be trivial in a retail park and very '
           'involved in a city centre building.',
 'prices': [
   ('Cafe or small kitchen', 'Single canopy, small front of house', [
     ('Front of house, one unit', '£2,450'),
     ('Two units, one condenser', '£4,400'),
     ('Extract only, short run', 'from £3,200'),
     ('Cellar cooling', 'from £2,600')]),
   ('Restaurant', 'Full kitchen and dining room', [
     ('Kitchen extract and make up', '£6,500'),
     ('Four cassette front of house', '£8,500'),
     ('Heat recovery ventilation', '£5,200'),
     ('Gas interlock system', 'from £1,400')]),
   ('Bar or multi floor', 'Larger venue or long duct run', [
     ('Six unit VRF', '£14,000'),
     ('Air handling unit', 'per project'),
     ('Long duct route to roof', 'per project'),
     ('Full fit out', 'per project')])],
 'price_note': '<strong>These are guide bands, not quotations.</strong> The duct '
               'route drives the price on most kitchen jobs. A discharge straight '
               'out of a rear wall is cheap. A run up four storeys of a city centre '
               'building to a roof termination, through a landlord\'s riser, is not. '
               'We establish that route at survey before anyone talks about a '
               'figure.',
 'du_nav': 'Regulations',
 'du_eyebrow': 'Safety and consent',
 'du_h2': 'The rules a commercial kitchen has to meet',
 'du_sub': 'Kitchen ventilation carries obligations that comfort cooling does not, '
           'and an insurer will ask about all three of these after a fire.',
 'duties': [
   ('Gas interlock',
    ['Where gas appliances sit under an extract canopy, BS 6173 requires an '
     'interlock so the gas supply cannot be on unless the ventilation is running '
     'and proving flow. It exists to stop combustion products collecting in a '
     'kitchen where nobody would notice.',
     'It is a commissioning item, not an optional extra, and it is one of the first '
     'things an environmental health officer or a gas engineer will look for.'],
    'The interlock is wired, proved and certificated as part of the handover pack '
    'rather than left to a separate visit.'),
   ('Ductwork and cleaning',
    ['Kitchen extract ductwork is specified to DW/172, which covers construction, '
     'fire dampers where the duct passes through compartments, and access panels at '
     'intervals so the whole run can be cleaned.',
     'Grease build up in a duct is a fire risk and a standard question on a '
     'commercial insurance policy. A duct with no access panels cannot be cleaned '
     'properly, which tends to become the operator\'s problem rather than the '
     'installer\'s.'],
    'Access panels go in at design stage. Retrofitting them into a finished ceiling '
    'costs several times as much.'),
   ('Noise, odour and planning',
    ['Extract discharge is a common source of complaint and a common planning '
     'condition, particularly on a city centre site with flats above or behind. '
     'Conditions usually cover the termination height, the noise limit at the '
     'nearest window, and odour control.',
     'Carbon filtration or an electrostatic unit handles odour where a condition '
     'requires it, and both need a maintenance regime to keep working.'],
    'Where a planning condition already exists, send it to us with the survey '
    'request and the design will be built to satisfy it.')],
 'faqs': [
   ('Why is the kitchen still hot when the extract is running?',
    'Almost always because there is no make up air. The canopy can only remove as '
    'much as can get back in, so without a designed supply the fan pulls against '
    'the building, the real extract rate falls well below the figure it was sold '
    'on, and the kitchen stays hot. Adding a make up air unit usually fixes it '
    'without touching the canopy.'),
   ('Do we legally need make up air?',
    'It is a design requirement rather than a single clause you can point at. A '
    'kitchen extract system has to work as designed, and it cannot without '
    'replacement air, so building control and any competent designer will expect '
    'it. The gas interlock also proves flow, and a starved system can fail to prove '
    'and shut your gas off.'),
   ('Can you work around service?',
    'Yes. Hospitality work is normally done overnight or on a closed day, with the '
    'kitchen handed back clean and the gas proved before service. Out of hours '
    'labour is charged at standard rates. A full fit out is programmed in writing '
    'so you know which sittings are affected.'),
   ('Will the council object to the extract?',
    'Possibly, and it is better to know first. Noise at the nearest residential '
    'window and cooking odour are the two usual conditions, and both are answered '
    'at design stage with termination height, the unit\'s sound data and odour '
    'control where required. Retrofitting that after a complaint is the expensive '
    'route.'),
   ('Do you do cellar cooling as well?',
    'Yes, and on a bar it should be designed alongside everything else rather than '
    'bolted on later. A cellar wants holding steadily in the low to mid teens, and '
    'the condenser needs a position where its heat and noise are not somebody '
    'else\'s problem.'),
   ('How often does kitchen ventilation need servicing?',
    'More often than comfort cooling. Grease filters are a routine cleaning job for '
    'your own team, while the ductwork and fan need a scheduled clean by a '
    'contractor at a frequency set by how heavily you cook. Our '
    '<a href="servicing">servicing plans</a> cover the cooling side, and the '
    'extract clean is scheduled against your insurer\'s requirement.')],
 'areas_line': 'We fit hospitality systems across Manchester city centre, Ancoats, '
               'the Northern Quarter, Chorlton and the wider North West',
 'service_type': 'Restaurant and commercial kitchen ventilation and air conditioning',
 'ld_desc': 'Kitchen extract, make up air, front of house cooling and cellar cooling '
            'for restaurants, bars and pubs in Manchester and across the North West.',
},

# -------------------------------------------------------------------- gyms
{
 'slug': 'gym-air-conditioning',
 'crumb': 'Gyms and studios',
 'eyebrow': 'Gyms, studios and leisure',
 'h1a': 'Gym and studio',
 'h1b': 'air conditioning',
 'title': 'Gym and Studio Air Conditioning Manchester | CoolIn',
 'desc': 'Cooling and ventilation for gyms and studios across Manchester and the '
         'North West. Sized on peak class size rather than floor area, with real air '
         'change.',
 'lede': 'Thirty people working hard in a room with no opening windows is a heat '
         'load nothing else in a building comes close to. Gyms need air changed as '
         'well as cooled, and sizing one on floor area is how you end up with a '
         'studio nobody wants to book.',
 'trust': [('Sized on people', 'not on square metres'),
           ('Air change', 'designed alongside the cooling'),
           ('Quiet running', 'specified to sit under the music')],
 'kf_lead': 'CoolIn designs, installs and maintains cooling and ventilation for '
            'gyms, boutique studios, martial arts spaces and leisure sites across '
            'Manchester and the North West, from a single spin room to a full floor '
            'of equipment.',
 'kf': [('Typical systems', 'High capacity ducted, cassettes, heat recovery ventilation'),
        ('Single studio', 'From £4,400 installed'),
        ('Gym floor', 'From £8,500 for four units'),
        ('Ventilation', 'From £5,200 for heat recovery'),
        ('Servicing', 'More frequent than an office, because of dust'),
        ('Fitting hours', 'Overnight and closed periods, standard rates')],
 'ch_eyebrow': 'What makes gyms different',
 'ch_h2': 'A gym is the highest heat load per square metre in the building',
 'ch_sub': 'Every other sector we work in is cooling a room. A gym is cooling '
           'people, and the difference in the numbers is not small. Get this wrong '
           'and no amount of adjusting the setpoint later will rescue it.',
 'challenges': [
   ('People are the load',
    'Someone sitting at a desk contributes roughly the heat of a small light bulb. '
    'The same person on a treadmill or a bike contributes several times that, and '
    'thirty of them together is a load on the scale of a small industrial process. '
    'Floor area tells you almost nothing here. Peak class size does.',
    'Sized on peak occupancy'),
   ('Cooling alone does not fix the air',
    'Recirculating chilled air keeps the temperature down and does nothing about '
    'carbon dioxide, humidity or smell, which are what members actually complain '
    'about. A busy studio with no fresh air feels stale even when the thermometer '
    'reads fine. That is a <a href="ventilation">ventilation</a> problem.',
    'Fresh air rate designed with the cooling'),
   ('Humidity is the part people forget',
    'Thirty people sweating in a closed room puts a lot of moisture into the air. '
    'Once humidity climbs, the room feels hotter than it reads, mirrors fog, and in '
    'a space with poor ventilation you get condensation and eventually a smell you '
    'cannot clean out.',
    'Latent load taken into account'),
   ('It cannot be loud, and it cannot blow on the mats',
    'A unit audible over a class is a complaint, and cold air dropping directly '
    'onto somebody lying on a mat in the stretch at the end is a bigger one. '
    'Positioning goes around how the room is used, and equipment gets specified on '
    'its sound level as well as its output.',
    'Positioned around the class layout')],
 'sy_h2': 'Which system suits a gym or studio',
 'sy_sub': 'High ceilings, high loads and a need for fresh air push gyms towards '
           'different kit from an office of the same size.',
 'systems': [
   ('High capacity ducted',
    'The usual answer on a gym floor. The plant sits out of the way, air is '
    'delivered through several grilles so no single spot gets blasted, and the duct '
    'run can be arranged around the rig and the lighting.'),
   ('Heat recovery ventilation',
    'Brings fresh air in and pushes stale air out while recovering most of the heat '
    'from the air leaving, so you are not paying to warm the outdoors in winter. On '
    'a busy gym this is not optional comfort, it is what keeps the room breathable.'),
   ('Ceiling cassettes',
    'Suit a boutique studio or a smaller room with a suspended ceiling, zoned per '
    'room so a spin class and a reformer studio can run at different temperatures '
    'at the same time.'),
   ('Destratification',
    'In a high bay unit the hot air collects at roof level where nobody benefits '
    'from it. Destratification fans bring it back down in winter and cut the '
    'heating bill, which is the same trick we use in '
    '<a href="warehouse-air-conditioning">warehouse spaces</a>.')],
 'co_h2': 'What gym air conditioning costs',
 'co_sub': 'Installed prices covering equipment, labour, commissioning and handover. '
           'Gyms vary widely with ceiling height, how much plant the roof will '
           'accept and how much ductwork the layout needs, so these are budget '
           'bands rather than quotations.',
 'prices': [
   ('Single studio', 'One class room', [
     ('Two units, one condenser', '£4,400'),
     ('Slim ducted, two zones', '£3,500'),
     ('Extract and make up air', 'from £2,400'),
     ('Single cassette, 3.5kW', '£2,450')]),
   ('Gym floor', 'Equipment floor plus studios', [
     ('Four unit system', '£8,500'),
     ('Heat recovery ventilation', '£5,200'),
     ('Six unit VRF', '£14,000'),
     ('High capacity ducted', 'from £7,800')]),
   ('Multi room site', 'Full club or leisure centre', [
     ('VRF, whole building', 'per project'),
     ('Air handling unit', 'per project'),
     ('Destratification', 'per project'),
     ('Plant replacement', 'per project')])],
 'price_note': '<strong>These are guide bands, not quotations.</strong> The number '
               'that moves a gym price most is peak class size, because that sets '
               'the capacity, and after that it is how much ductwork the ceiling '
               'height and rig layout force on the design. We ask for your class '
               'timetable at survey, which tells us more than the floor plan does.',
 'du_nav': 'Running it',
 'du_eyebrow': 'Maintenance and duties',
 'du_h2': 'Keeping it working in a dusty, heavily used building',
 'du_sub': 'Gym plant works harder than almost anything else we maintain, in an '
           'environment that is unusually hard on filters. A servicing interval '
           'written for an office is the wrong interval here.',
 'duties': [
   ('Filters and servicing frequency',
    ['Chalk, rubber dust off the flooring and skin particles load a filter far '
     'faster than an office does. A blocked filter cuts airflow, which cuts '
     'capacity, which is why a gym system that was fine in year one can feel '
     'undersized in year two without anything having failed.',
     'Most gyms we look after need more visits a year than the standard office '
     'schedule, and the filter clean is the reason.'],
    'Our <a href="servicing">servicing plans</a> start at £89 per indoor unit per '
    'year, and we set the visit frequency against how the building is actually '
    'used rather than a default.'),
   ('Air quality and how it feels',
    ['Carbon dioxide is the usual proxy for whether a room has enough fresh air, '
     'and it climbs quickly in a packed studio with the door shut. High readings '
     'track closely with the stale, heavy feeling members describe.',
     'Monitoring it is cheap and it gives you a number to design against, instead '
     'of a debate about whether the room feels stuffy.'],
    'Where a room is already built and ventilation cannot be added easily, '
    'increasing the fresh air share on the existing system is often the practical '
    'fix.'),
   ('F-Gas and TM44',
    ['A gym with several large units frequently crosses the 5 tonne CO2 equivalent '
     'line that brings leak checking and record keeping duties, and a VRF system '
     'almost certainly does.',
     'The TM44 threshold of 12kW of effective rated output across the building is '
     'crossed by most gym floors, so an inspection by an accredited assessor is due '
     'at least every five years.'],
    'We work out where your building sits against both thresholds at survey and put '
    'it in writing.')],
 'faqs': [
   ('How much cooling does a studio of thirty people need?',
    'Far more than the floor area suggests, because the people are the load. A '
    'person exercising hard gives off several times the heat of the same person at '
    'a desk, so peak class size is the number the design starts from. A small '
    'studio running full classes can need more capacity than an open plan office '
    'three times its size.'),
   ('Will members hear it over the class?',
    'They should not. Equipment is specified on its sound level as well as its '
    'output, and ducted systems keep the noisy part of the kit away from the room. '
    'The common mistake is a single undersized unit running flat out permanently, '
    'which is both louder and less effective than properly sized plant modulating.'),
   ('Do we need ventilation as well as cooling?',
    'In a busy gym, yes. Cooling recirculates air and controls temperature. It does '
    'not remove carbon dioxide, moisture or smell, and those are what members '
    'notice. Heat recovery ventilation brings fresh air in without throwing the '
    'heating away with the stale air.'),
   ('Can you heat a hot yoga or bikram room?',
    'Yes, and it is a specific design rather than a normal system turned up. Those '
    'rooms need controlled heat and controlled humidity held steadily, plus enough '
    'air change between classes to clear the room. Tell us the temperature and '
    'humidity you want to hold and we will design to it.'),
   ('How often should gym air conditioning be serviced?',
    'More often than an office. Dust loading on filters is the reason, and a '
    'blocked filter directly reduces the cooling you get. We set the interval '
    'against your opening hours and class density, and most gym sites end up on '
    'more than one visit a year.'),
   ('Can you fit it without closing?',
    'Usually. Studio by studio is the normal approach, working overnight or during '
    'a quiet block so only one room is out at a time. A full gym floor is '
    'programmed in writing against your timetable, and out of hours labour is '
    'charged at standard rates.')],
 'areas_line': 'We fit gym and studio systems across Manchester, Salford, Stockport, '
               'Altrincham and the wider North West',
 'service_type': 'Gym and fitness studio air conditioning and ventilation',
 'ld_desc': 'Cooling and ventilation for gyms, boutique studios and leisure sites in '
            'Manchester and across the North West, sized on peak occupancy rather '
            'than floor area.',
},

# ------------------------------------------------------------ server rooms
{
 'slug': 'server-room-cooling',
 'crumb': 'Server rooms',
 'eyebrow': 'Server, comms and plant rooms',
 'h1a': 'Server room and',
 'h1b': 'comms room cooling',
 'title': 'Server Room Cooling Manchester | CoolIn',
 'desc': 'Close control cooling for server and comms rooms across Manchester and the '
         'North West. Runs year round, with redundancy and alarms where it matters.',
 'lede': 'A server room runs the same load at four in the morning in January as it '
         'does on the hottest afternoon of the year, and it fails expensively when '
         'it gets hot. Comfort cooling is not designed for that. Close control is, '
         'and the difference shows up the first time something goes wrong at a '
         'weekend.',
 'trust': [('Year round', 'no seasonal shutdown, ever'),
           ('Redundancy', 'a second unit where downtime costs'),
           ('Alarms', 'you hear about it before the kit does')],
 'kf_lead': 'CoolIn designs, installs and maintains cooling for server rooms, comms '
            'rooms and small data suites across Manchester and the North West, from '
            'a single rack in a cupboard to a room running on N+1 with remote '
            'monitoring.',
 'kf': [('Typical systems', 'Close control, in row, dedicated splits on rotation'),
        ('Close control', 'From £9,000 installed'),
        ('Comms cupboard', 'From £2,600 for a dedicated unit'),
        ('Recommended range', '18C to 27C at the rack inlet'),
        ('Servicing', 'Usually four visits a year, not one'),
        ('Monitoring', 'Temperature alarm to phone or email')],
 'ch_eyebrow': 'Why it is a different job',
 'ch_h2': 'Why a normal air conditioning unit is the wrong answer',
 'ch_sub': 'This is the single most common thing we are asked to put right. A '
           'comfort unit will cool a server room, right up until the day it does '
           'not, and the way it fails is specific and predictable.',
 'challenges': [
   ('The load never stops',
    'Comfort cooling is built for a room full of people that empties at six and is '
    'shut at the weekend. A server room is at full load every hour of every day, '
    'including the coldest week of the year. Run a domestic split like that and you '
    'are running it well outside what it was designed for.',
    'Equipment rated for continuous duty'),
   ('It will not run in winter',
    'Most comfort units are not built to cool when it is near freezing outside, and '
    'will refuse to run or trip on low pressure. That is fine in an office, which '
    'wants heating in January. In a server room it means the cooling stops in the '
    'one situation where nobody is watching, and the room climbs.',
    'Low ambient operation specified'),
   ('One unit is one point of failure',
    'When the single unit in the room fails, the clock starts immediately, and a '
    'small room with several racks in it heats up quickly. Two smaller units '
    'sharing the load, alternating so both stay exercised, means a failure is an '
    'inconvenience rather than an outage.',
    'N+1 with lead and lag rotation'),
   ('Nobody finds out until it is too late',
    'Server rooms have no occupants to notice. Without a temperature alarm the '
    'first sign of a failure is usually kit shutting itself down, often on a Friday '
    'night. A sensor and an alert cost very little against what an unplanned outage '
    'costs.',
    'Temperature alarm to phone or email')],
 'sy_h2': 'What we install in a server or comms room',
 'sy_sub': 'The right answer scales with what is in the room and what an hour of '
           'downtime costs you. A comms cupboard and a room of racks are different '
           'problems.',
 'systems': [
   ('Close control cooling',
    'Purpose built for technical spaces. Holds tighter temperature and humidity '
    'bands than comfort equipment, runs continuously year round, and is designed to '
    'handle the dry, high sensible load a room of servers actually presents.'),
   ('N+1 redundancy',
    'A second unit sized so either can carry the room alone, with a controller '
    'alternating lead and lag so both stay exercised and neither sits idle for '
    'months. Standard on any room where an outage has a real cost.'),
   ('Dedicated splits on rotation',
    'For a smaller comms room, two dedicated units specified for low ambient '
    'operation and alternated weekly. Considerably cheaper than close control and a '
    'sound answer where the room is a cupboard rather than a suite.'),
   ('Monitoring and alarms',
    'Temperature and, where it matters, humidity sensing with an alert to a phone '
    'or an email address. The cheapest part of the whole job and the part that most '
    'often turns a disaster into a callout.')],
 'co_h2': 'What server room cooling costs',
 'co_sub': 'Installed prices covering equipment, labour, commissioning and handover. '
           'A technical room is priced on its heat load in kilowatts, on how much '
           'redundancy you want, and on where the condenser can go, so these are '
           'budget bands rather than quotations.',
 'prices': [
   ('Comms cupboard', 'A rack or two, low criticality', [
     ('Single dedicated unit', 'from £2,600'),
     ('Two units on rotation', 'from £4,900'),
     ('Temperature alarm', 'from £320'),
     ('Ventilation only', 'per project')]),
   ('Server room', 'Several racks, business critical', [
     ('Close control, single unit', 'from £9,000'),
     ('Close control, N+1 pair', 'per project'),
     ('Monitoring and alerting', 'from £320'),
     ('Quarterly service plan', 'from £229 per unit')]),
   ('Larger suite', 'Multi rack or high density', [
     ('In row cooling', 'per project'),
     ('Containment and airflow', 'per project'),
     ('Plant replacement', 'per project'),
     ('Resilience upgrade', 'per project')])],
 'price_note': '<strong>These are guide bands, not quotations.</strong> A server '
               'room quote starts from the actual heat load, which we work out from '
               'the connected load of the kit in the room rather than from its '
               'floor area. That number, plus whether you want redundancy, decides '
               'almost everything else. The survey costs nothing.',
 'du_nav': 'Resilience',
 'du_eyebrow': 'Operation and duties',
 'du_h2': 'Keeping a technical room reliable',
 'du_sub': 'The design gets you a room that works. These three are what keep it '
           'working, and they are where most of the rooms we inherit have been let '
           'down.',
 'duties': [
   ('Temperature and humidity targets',
    ['The widely used industry guidance recommends keeping the air entering the '
     'equipment between roughly 18C and 27C. Running colder than that wastes '
     'electricity without making the hardware any happier.',
     'Humidity matters in both directions. Too high and you risk condensation on '
     'cold surfaces. Too low and static becomes a genuine hazard when somebody '
     'works in the racks.'],
    'What actually matters is the temperature at the rack inlet, not the reading on '
    'a wall thermostat across the room, which is why sensor position is part of the '
    'design.'),
   ('Servicing frequency',
    ['A room running at full load every hour of the year needs looking at more '
     'often than an office. Most server rooms we maintain are on four visits a '
     'year, checking filters, coil condition, refrigerant charge, drain operation '
     'and the alarm itself.',
     'Testing the alarm is the part most often skipped, and an alarm nobody has '
     'proved is not resilience.'],
    'Our <a href="servicing">commercial servicing plan</a> covers quarterly '
    'attendance, and we test the failover on rooms running a lead and lag pair.'),
   ('F-Gas duties',
    ['Close control systems hold more refrigerant than a comfort unit, so a server '
     'room crosses the 5 tonne CO2 equivalent threshold more readily than most '
     'spaces of its size. Past that line the operator has to arrange leak checks '
     'and keep records.',
     'Automatic leak detection can extend the interval between manual checks on '
     'larger systems, which is worth knowing before specifying.'],
    'The thresholds in full are on the <a href="commercial#compliance">commercial '
    'page</a>, and we work out where your system sits at survey.')],
 'faqs': [
   ('Can I just use a normal split unit in my server room?',
    'For a small comms cupboard it can work, provided the unit is specified for low '
    'ambient operation so it still cools when it is near freezing outside, and '
    'provided you accept that a failure means downtime. Standard comfort equipment '
    'installed without that specification is the most common cause of the winter '
    'failures we get called to.'),
   ('What temperature should a server room be?',
    'Industry guidance recommends air entering the equipment between roughly 18C '
    'and 27C. Many rooms are run far colder than they need to be, which costs real '
    'money in electricity and gains nothing. The measurement that counts is at the '
    'rack inlet rather than on a wall.'),
   ('Do I need two units?',
    'It depends entirely on what an hour of downtime costs you. If the room only '
    'runs a switch and a file server, one properly specified unit plus an alarm is '
    'reasonable. If the business stops when the room stops, two units sized so '
    'either can carry the load alone is the only sensible answer.'),
   ('What happens if the cooling fails overnight?',
    'With no alarm, the room heats until the equipment protects itself or fails, '
    'and you find out on Monday. With a sensor and an alert you get a message while '
    'there is still time to open a door, bring in temporary cooling or shut things '
    'down in an orderly way. It is the cheapest resilience you can buy.'),
   ('How often should it be serviced?',
    'Usually four times a year rather than once. The load is constant, the run '
    'hours are far higher than comfort equipment, and the alarm needs proving as '
    'well as the cooling. Quarterly attendance is what our commercial plan is built '
    'around.'),
   ('Can you cool a room that already has equipment running?',
    'Yes. We plan the work so the room is never left without cooling for longer '
    'than it can safely tolerate, using temporary cooling during the changeover '
    'where the heat load makes that necessary. That sequencing is set out in the '
    'quote rather than improvised on the day.')],
 'areas_line': 'We cool server and comms rooms across Manchester, Salford Quays, '
               'Warrington, Stockport and the wider North West',
 'service_type': 'Server room and comms room cooling',
 'ld_desc': 'Close control cooling, redundancy and monitoring for server rooms and '
            'comms rooms in Manchester and across the North West, designed for a '
            'continuous year round load.',
},

# ------------------------------------------------------------- industrial
{
 'slug': 'warehouse-air-conditioning',
 'crumb': 'Warehouse and industrial',
 'eyebrow': 'Warehouse, industrial and workshops',
 'h1a': 'Warehouse and industrial',
 'h1b': 'air conditioning',
 'title': 'Warehouse Air Conditioning Manchester | CoolIn',
 'desc': 'Spot cooling, destratification and ventilation for warehouses and '
         'industrial units across Manchester and the North West. Cooling where '
         'people work.',
 'lede': 'Conditioning the full volume of a warehouse is rarely worth what it '
         'costs. Cooling the places people actually stand, bringing the heat back '
         'down from roof level in winter, and ventilating the rest usually gets you '
         'a workable building for a fraction of the money.',
 'trust': [('Spot cooling', 'where people work, not the whole volume'),
           ('Destratification', 'heat brought back down in winter'),
           ('Heavy duty', 'plant specified for a dusty building')],
 'kf_lead': 'CoolIn designs and installs cooling, destratification and ventilation '
            'for warehouses, workshops, production areas and industrial units '
            'across Manchester and the North West, including the mezzanine offices '
            'that sit inside them.',
 'kf': [('Typical systems', 'Spot cooling, high level ducted, destratification, ventilation'),
        ('Mezzanine office', 'From £2,450 installed'),
        ('Zone or spot cooling', 'Priced per zone'),
        ('Workplace guidance', 'No legal maximum, 16C suggested minimum'),
        ('Plant', 'Specified for dust and continuous running'),
        ('Servicing', 'Filter intervals set against the environment')],
 'ch_eyebrow': 'What makes industrial different',
 'ch_h2': 'Why cooling the whole building is usually the wrong plan',
 'ch_sub': 'The instinct is to ask what it costs to air condition the warehouse. '
           'The better question is which parts of it actually need conditioning, '
           'because the answer is almost never all of it.',
 'challenges': [
   ('The volume is enormous and mostly empty',
    'A high bay unit holds a huge amount of air above head height that nobody '
    'benefits from cooling. Sizing plant for the full volume produces a capital '
    'cost and a running cost out of all proportion to the comfort it buys.',
    'Cooling targeted at occupied zones'),
   ('Heat collects where nobody is standing',
    'Warm air rises and sits at roof level, so in winter you can have a roof space '
    'well above 20C while the floor is cold, and you are paying to heat both. '
    'Destratification fans push that layer back down and often pay for themselves '
    'on the heating bill alone.',
    'Stratification measured at survey'),
   ('The heat often comes from the process',
    'Ovens, compressors, presses and welding bays put heat into the building '
    'continuously and in one place. Extracting or containing it at source is nearly '
    'always cheaper than cooling the whole space afterwards, and it usually works '
    'better.',
    'Heat dealt with at source where possible'),
   ('Mezzanine offices are their own building',
    'A boxed office sitting inside a warehouse gets the warm roof layer on top of '
    'its own load, with no external wall on most sides. It behaves nothing like the '
    'floor below it and needs <a href="office-air-conditioning">its own system</a> '
    'rather than a share of anything.',
    'Mezzanines designed separately')],
 'sy_h2': 'What actually works in an industrial building',
 'sy_sub': 'Four approaches, and most sites end up with a combination rather than '
           'one of them. Which combination depends on where the people and the heat '
           'are.',
 'systems': [
   ('Spot and zone cooling',
    'Cooling delivered to packing benches, picking faces, workshop bays and other '
    'places people stand for hours, rather than to the volume as a whole. Far less '
    'capacity, far less running cost, and the comfort lands where it is noticed.'),
   ('Destratification',
    'High level fans that bring the warm layer at roof level back down to where '
    'people are. Cheap to install, cuts the heating demand noticeably in a tall '
    'building, and makes the floor feel better in winter without adding heat.'),
   ('High level ducted',
    'Where a whole area genuinely does need conditioning, plant at high level '
    'feeding ducted distribution keeps equipment out of the way of racking, forklift '
    'routes and cranes.'),
   ('Ventilation and extract',
    'Often the better answer in a workshop. Removing process heat, fume or dust at '
    'source through <a href="ventilation">extract and make up air</a> deals with the '
    'cause instead of paying to cool the result.')],
 'co_h2': 'What industrial cooling costs',
 'co_sub': 'Installed prices covering equipment, labour, commissioning and handover. '
           'Industrial work is quoted per project more than any other sector, '
           'because access equipment, height and the electrical supply available '
           'change the figure substantially.',
 'prices': [
   ('Offices and small areas', 'Mezzanine, site office, control room', [
     ('Single cassette, 3.5kW', '£2,450'),
     ('Wall unit, 5kW', '£2,280'),
     ('Two units, one condenser', '£4,400'),
     ('Slim ducted, two zones', '£3,500')]),
   ('Working zones', 'Benches, bays and picking faces', [
     ('Spot cooling per zone', 'per project'),
     ('Destratification', 'per project'),
     ('Extract and make up air', 'from £2,400'),
     ('Heat recovery ventilation', '£5,200')]),
   ('Whole area', 'Production hall or conditioned store', [
     ('High level ducted', 'per project'),
     ('Air handling unit', 'per project'),
     ('Process heat extract', 'per project'),
     ('Plant replacement', 'per project')])],
 'price_note': '<strong>These are guide bands, not quotations.</strong> Height '
               'drives industrial prices. Work above a certain level needs access '
               'equipment, a permit regime and often a second pair of hands, and '
               'that shows up in the labour before any equipment is priced. We '
               'establish access at survey so the written price holds.',
 'du_nav': 'Workplace',
 'du_eyebrow': 'Duties and comfort',
 'du_h2': 'Workplace temperature, and what the law actually says',
 'du_sub': 'This comes up on every industrial survey, usually as a claim about a '
           'legal maximum temperature. It is worth being clear about what the rules '
           'do and do not require.',
 'duties': [
   ('There is no legal maximum temperature',
    ['Workplace regulations require a reasonable temperature rather than a specific '
     'one, and there is no upper figure in law that forces an employer to send '
     'people home. The approved guidance suggests a minimum of around 16C, dropping '
     'to about 13C where the work involves severe physical effort.',
     'What does apply is the general duty to assess the risk and act on it. In a '
     'building where people work hard in high summer heat, that assessment is a '
     'real obligation even though no thermometer reading triggers it '
     'automatically.'],
    'In practice the argument for cooling an industrial space is usually '
    'productivity, error rates and staff retention rather than a rule somebody can '
    'point at.'),
   ('Plant that survives the environment',
    ['Standard equipment in a dusty building blocks up fast, and a blocked coil or '
     'filter cuts capacity before it causes an outright failure. Filter grade, coil '
     'coating and unit position all need specifying against the actual environment '
     'rather than a catalogue default.',
     'Where forklifts operate, physical protection for pipework, isolators and low '
     'level plant belongs in the design rather than being added after the first '
     'impact.'],
    'We set servicing intervals against how dirty the building actually is, not '
    'against a standard office schedule.'),
   ('F-Gas and TM44',
    ['Industrial sites frequently have air conditioning spread across offices, '
     'control rooms and production areas, and TM44 counts the whole building. The '
     '12kW threshold is crossed easily once several areas are added together.',
     'Process refrigeration and cold storage sit under their own separate regime '
     'and are a different trade from comfort cooling, so they are quoted and '
     'maintained separately.'],
    'We work out the total across the site at survey and tell you where you stand '
    'against both thresholds.')],
 'faqs': [
   ('Is there a legal maximum workplace temperature in the UK?',
    'No. The regulations require a reasonable temperature rather than naming an '
    'upper limit, so there is no figure at which work must legally stop. The '
    'approved guidance does suggest a minimum of around 16C, or about 13C where the '
    'work is physically demanding. The duty to assess and control the risk still '
    'applies in hot conditions.'),
   ('Can you air condition a whole warehouse?',
    'Technically yes, and for most buildings it is not worth what it costs. The '
    'volume above head height is the problem. Cooling the zones where people '
    'actually work, ventilating the rest and dealing with process heat at source '
    'gets a far better result for the money in nearly every case.'),
   ('What is destratification and is it worth it?',
    'Warm air collects at roof level where nobody feels it. Destratification fans '
    'push that layer back down to floor level. In a tall building it can cut heating '
    'demand noticeably and makes the working area feel warmer in winter without '
    'adding any heat, which is why it is often the first thing we recommend.'),
   ('Can you cool just the packing area?',
    'Yes, and that is normally the right approach. Spot and zone cooling delivers '
    'capacity where people stand for hours, at a fraction of the capital and running '
    'cost of conditioning the whole space. The zones are agreed at survey from how '
    'the building is used.'),
   ('Do you do cold stores and process refrigeration?',
    'Those sit under a separate regime from comfort cooling and are a different '
    'trade, so we quote and maintain them separately rather than folding them into '
    'a comfort cooling package. Tell us what you need at survey and we will be '
    'straight with you about scope.'),
   ('Will the dust wreck the units?',
    'It will shorten their life if the plant was specified for an office. Filter '
    'grade, coil protection and where the unit draws its air from all need choosing '
    'against the real environment, and the servicing interval needs to match. Done '
    'properly, industrial plant lasts. Done from a catalogue, it does not.')],
 'areas_line': 'We work on industrial sites across Trafford Park, Salford, '
               'Warrington, Wigan, Bolton and the wider North West',
 'service_type': 'Warehouse and industrial air conditioning and ventilation',
 'ld_desc': 'Spot cooling, destratification, high level ducted systems and '
            'ventilation for warehouses, workshops and industrial units in '
            'Manchester and across the North West.',
},

]
