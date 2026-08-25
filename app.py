import streamlit as st
import pandas as pd
import datetime
import io

st.set_page_config(page_title="UID Timetable Generator", layout="wide")

# ---------------------------------------------------------
# MASTER DATA: COURSES & CURRICULUM
# ---------------------------------------------------------
MASTER_COURSES = [
    # 3rd Sem B.Des PD
    {"code": "UC012030001", "title": "Personality Development", "program": "B.Design (Hons.) Product Design", "program_code": "1019", "sem": "III"},
    {"code": "31203001203", "title": "Design Research", "program": "B.Design (Hons.) Product Design", "program_code": "1019", "sem": "III"},
    {"code": "31203006211", "title": "Product Visualization", "program": "B.Design (Hons.) Product Design", "program_code": "1019", "sem": "III"},
    {"code": "31203006212", "title": "Form, Aesthetic and Emotion", "program": "B.Design (Hons.) Product Design", "program_code": "1019", "sem": "III"},
    {"code": "31203006207", "title": "Studio- Human Centric Design", "program": "B.Design (Hons.) Product Design", "program_code": "1019", "sem": "III"},
    {"code": "31203006213", "title": "Design Articulation with AI", "program": "B.Design (Hons.) Product Design", "program_code": "1019", "sem": "III"},
    {"code": "31203006214", "title": "Indian Design System", "program": "B.Design (Hons.) Product Design", "program_code": "1019", "sem": "III"},

    # 5th Sem B.Des PD
    {"code": "UC013050001", "title": "CAID", "program": "B.Design (Hons.) Product Design", "program_code": "1019", "sem": "V"},
    {"code": "31305001325", "title": "Conceptualization and Characterization", "program": "B.Design (Hons.) Product Design", "program_code": "1019", "sem": "V"},
    {"code": "31305001326", "title": "Ad Film Production", "program": "B.Design (Hons.) Product Design", "program_code": "1019", "sem": "V"},
    {"code": "31305001327", "title": "Fashion Styling", "program": "B.Design (Hons.) Product Design", "program_code": "1019", "sem": "V"},
    {"code": "31305001328", "title": "Space Perception", "program": "B.Design (Hons.) Product Design", "program_code": "1019", "sem": "V"},
    {"code": "31305001329", "title": "UX/UI", "program": "B.Design (Hons.) Product Design", "program_code": "1019", "sem": "V"},
    {"code": "31305001330", "title": "The Art of Delightful Design", "program": "B.Design (Hons.) Product Design", "program_code": "1019", "sem": "V"},
    {"code": "31305001331", "title": "Speed Modelling in Clay", "program": "B.Design (Hons.) Product Design", "program_code": "1019", "sem": "V"},
    {"code": "31305006322", "title": "Human Factors", "program": "B.Design (Hons.) Product Design", "program_code": "1019", "sem": "V"},
    {"code": "31305006323", "title": "Portfolio with AI", "program": "B.Design (Hons.) Product Design", "program_code": "1019", "sem": "V"},
    {"code": "31305006324", "title": "Studio- Humanizing Technology", "program": "B.Design (Hons.) Product Design", "program_code": "1019", "sem": "V"},
    {"code": "31305006325", "title": "Experience Design", "program": "B.Design (Hons.) Product Design", "program_code": "1019", "sem": "V"},
    {"code": "31305006326", "title": "Packaging Design", "program": "B.Design (Hons.) Product Design", "program_code": "1019", "sem": "V"},
    {"code": "31305006327", "title": "Speculative design", "program": "B.Design (Hons.) Product Design", "program_code": "1019", "sem": "V"},

    # 7th Sem B.Des PD
    {"code": "31407001400", "title": "Design Management", "program": "B.Design (Hons.) Product Design", "program_code": "1019", "sem": "VII"},
    {"code": "31407006403", "title": "Internship", "program": "B.Design (Hons.) Product Design", "program_code": "1019", "sem": "VII"},
    {"code": "31407006404", "title": "Studio- System Analysis and Design", "program": "B.Design (Hons.) Product Design", "program_code": "1019", "sem": "VII"},

    # 1st Sem M.Des ID
    {"code": "32101001500", "title": "Professional Communication", "program": "M.Design (Industrial Design)", "program_code": "1025", "sem": "I"},
    {"code": "32101002501", "title": "Design Foundation", "program": "M.Design (Industrial Design)", "program_code": "1025", "sem": "I"},
    {"code": "32101002502", "title": "Form Studies", "program": "M.Design (Industrial Design)", "program_code": "1025", "sem": "I"},
    {"code": "32101002503", "title": "Design Studio I", "program": "M.Design (Industrial Design)", "program_code": "1025", "sem": "I"},
    {"code": "32101002504", "title": "Design Prototyping", "program": "M.Design (Industrial Design)", "program_code": "1025", "sem": "I"},
    {"code": "32101002505", "title": "Frugal Innovation", "program": "M.Design (Industrial Design)", "program_code": "1025", "sem": "I"},
    {"code": "32101002506", "title": "Emergent Technology", "program": "M.Design (Industrial Design)", "program_code": "1025", "sem": "I"},
    {"code": "32101002507", "title": "CAID & Visualization with AI", "program": "M.Design (Industrial Design)", "program_code": "1025", "sem": "I"},

    # 3rd Sem M.Des ID
    {"code": "32203001602", "title": "Internship", "program": "M.Design (Industrial Design)", "program_code": "1025", "sem": "III"},
    {"code": "32203001603", "title": "Entrepreneurship", "program": "M.Design (Industrial Design)", "program_code": "1025", "sem": "III"},
    {"code": "32203001604", "title": "Research Methodology", "program": "M.Design (Industrial Design)", "program_code": "1025", "sem": "III"},
    {"code": "32203002609", "title": "User Experience Design", "program": "M.Design (Industrial Design)", "program_code": "1025", "sem": "III"},
    {"code": "32203002610", "title": "Studio- Design and Technology", "program": "M.Design (Industrial Design)", "program_code": "1025", "sem": "III"},
    {"code": "32203002611", "title": "Lighting Design", "program": "M.Design (Industrial Design)", "program_code": "1025", "sem": "III"},
    {"code": "32203002612", "title": "Craft and Technology", "program": "M.Design (Industrial Design)", "program_code": "1025", "sem": "III"},
]

# Search Catalog options mapping
COURSE_OPTIONS = {}
for c in MASTER_COURSES:
    label = f"{c['code']} - {c['title']} ({c['sem']} Sem {c['program']})"
    COURSE_OPTIONS[label] = c
COURSE_OPTIONS["✏️ [Custom / Manual Entry]"] = None

# Master Faculty Directory
DEFAULT_FACULTY_LIST = {
    "-- None / Leave Empty --": "",
    "✏️ [Manual / Custom Entry]": "CUSTOM",
    "Aakanksha Batra (15122)": "15122",
    "Aayush Amit Bhingare (15184)": "15184",
    "Abhishek Karmakar (15254)": "15254",
    "Aditya Chauhan (10084)": "10084",
    "Aditya Lingam (15067)": "15067",
    "Agnivesh Sharma (15206)": "15206",
    "Aigers Liepins (15183)": "15183",
    "Ajay Bisht (15075)": "15075",
    "Akhil Tamta (15153)": "15153",
    "Anahita Suri (15027)": "15027",
    "Anthony Alphonso (15235)": "15235",
    "Anu Jain (15204)": "15204",
    "Anupam Tiwari (15212)": "15212",
    "Anupam Tomer (15234)": "15234",
    "Arjun Sengar (15124)": "15124",
    "Arshkirat Singh Gill (15279)": "15279",
    "Arun Gupta (15187)": "15187",
    "Arun Soman (15172)": "15172",
    "Arunita Paul (15166)": "15166",
    "Ashish Kumar (15214)": "15214",
    "Ashish Nar (15325)": "15325",
    "Ashuj Chawda (15506)": "15506",
    "Ashwani(Alex) Pawar (15215)": "15215",
    "DA Siddharth (15445)": "15445",
    "Dhanush Kumar (15497)": "15497",
    "Diksha Singh (15250)": "15250",
    "Dr. Arunita Paul (15166)": "15166",
    "Dr. Shilpi Bora (15324)": "15324",
    "Hirock Jyoti Roy (3438)": "3438",
    "Kishan Chavda (15177)": "15177",
    "Malekulashter (15342)": "15342",
    "Mark Timothy (15231)": "15231",
    "Navneet Kumar (15095)": "15095",
    "Niral Desai (15104)": "15104",
    "Parag Sarma (15182)": "15182",
    "Pradeep Patil (15133)": "15133",
    "Prem Gunjan (15109)": "15109",
    "Rakesh Sharma (10039)": "10039",
    "Ravi N Sachula (3472)": "3472",
    "Sabyasachi Biswas (15224)": "15224",
    "Sachin Khankhoje (15121)": "15121",
    "Sharad Shekar Shetty (15044)": "15044",
    "Shoeb Iqbal Khan (15255)": "15255",
    "Shyambihari Shankarprasad Prajapati (15005)": "15005",
    "Sree Hari B Lal (15546)": "15546",
    "Sreya Acharyya (15461)": "15461",
    "Subhash Chandra Bose Yalala (15435)": "15435",
    "Sundar Mahalingam (10098)": "10098",
    "Sweta Raj (15222)": "15222",
    "Umang Shah (15069)": "15069",
    "Varshin Vala (3333)": "3333",
    "Venkateshwaran N (15201)": "15201",
    "Vipul Nagjibhai Prajapati (3479)": "3479",
    "Vipul Vinayak Jadhav (15500)": "15500"
}

DAYS_MAP = {"Mon": 0, "Tue": 1, "Wed": 2, "Thu": 3, "Fri": 4, "Sat": 5}
SEMESTERS = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII"]

# ---------------------------------------------------------
# UI LAYOUT
# ---------------------------------------------------------
st.title("UID Timetable Auto-Population Tool")
st.caption("Auto-generate timetable matrices with curriculum search, faculty lookup, and Thursday half-day logic.")

col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.subheader("1. Session & Program Setup")
    
    today = datetime.date.today()
    c_d1, c_d2 = st.columns(2)
    start_date = c_d1.date_input("Start Date", today)
    end_date = c_d2.date_input("End Date", today + datetime.timedelta(days=4))
    
    selected_days = st.multiselect(
        "Active Days of Week", 
        options=list(DAYS_MAP.keys()), 
        default=["Mon", "Tue", "Wed", "Thu", "Fri"]
    )
    
    thursday_half_day = st.checkbox("Thursday Afternoon Off (Half Day)", value=True)
    
    st.subheader("2. Subject / Course Search")
    selected_course_label = st.selectbox("Search by Course Code or Subject Name", list(COURSE_OPTIONS.keys()))
    course_obj = COURSE_OPTIONS[selected_course_label]
    
    if course_obj is not None:
        c_code_val = course_obj["code"]
        c_prog_val = course_obj["program_code"]
        c_sem_val = course_obj["sem"]
        st.success(f"**Selected:** {course_obj['title']} | Code: `{c_code_val}` | Program: `{c_prog_val}` | Sem: `{c_sem_val}`")
    else:
        c_code_val = ""
        c_prog_val = "1019"
        c_sem_val = "V"

    c_f1, c_f2 = st.columns(2)
    program_code = c_f1.text_input("Program Code", value=c_prog_val)
    semester_code = c_f2.selectbox("Semester", SEMESTERS, index=SEMESTERS.index(c_sem_val) if c_sem_val in SEMESTERS else 0)

    c_f3, c_f4 = st.columns(2)
    course_code = c_f3.text_input("Course Code", value=c_code_val)
    course_type = c_f4.selectbox("Course Type", ["MANDATORY", "ELECTIVE"], index=0)

    c_slot1, c_slot2 = st.columns(2)
    morning_slot_type = c_slot1.selectbox("Morning Slot (09:30 - 13:00)", ["THEORY", "PRACTICAL"], index=0)
    afternoon_slot_type = c_slot2.selectbox("Afternoon Slot (13:55 - 17:30)", ["PRACTICAL", "THEORY"], index=0)
    academic_block = st.text_input("Academic Block", value="F")

with col_right:
    st.subheader("3. Section & Faculty Allocations")
    num_sections = st.slider("Number of Sections in Batch", min_value=1, max_value=5, value=4)
    
    section_labels = ["A", "B", "C", "D", "E"][:num_sections]
    section_inputs = []
    
    st.write("Assign Faculty & Studio Room per Section:")
    for sec in section_labels:
        st.markdown(f"**Section {sec}**")
        s_col1, s_col2 = st.columns([3, 2])
        
        selected_fac_label = s_col1.selectbox(
            f"Faculty for Sec {sec}", 
            options=list(DEFAULT_FACULTY_LIST.keys()), 
            key=f"fac_select_{sec}"
        )
        
        if selected_fac_label == "✏️ [Manual / Custom Entry]":
            fac_code = s_col1.text_input(f"Type Custom Faculty Code (Sec {sec})", key=f"fac_custom_{sec}")
        elif selected_fac_label == "-- None / Leave Empty --":
            fac_code = ""
        else:
            fac_code = DEFAULT_FACULTY_LIST[selected_fac_label]
            
        room = s_col2.text_input(f"Room Allocation (Sec {sec})", key=f"room_{sec}", placeholder="e.g. F2, E10")
        
        section_inputs.append({
            "section": sec,
            "faculty_code": fac_code.strip() if fac_code else None,
            "room": room.strip() if room else None
        })

# ---------------------------------------------------------
# GENERATION ENGINE
# ---------------------------------------------------------
st.markdown("---")

if st.button("Generate Timetable", type="primary", use_container_width=True):
    if not course_code:
        st.error("Please enter or select a Course Code.")
    elif start_date > end_date:
        st.error("Start Date must be before or equal to End Date.")
    else:
        active_day_ints = [DAYS_MAP[d] for d in selected_days]
        rows = []
        cur_date = start_date
        
        while cur_date <= end_date:
            if cur_date.weekday() in active_day_ints:
                is_thursday = (cur_date.weekday() == 3)
                date_str = cur_date.strftime("%Y-%m-%d")
                shift_timing = "09:30 TO 13:00" if (is_thursday and thursday_half_day) else "09:30 TO 17:30"
                
                for sec in section_inputs:
                    # Slot 1: Morning Slot
                    rows.append({
                        "Date": date_str,
                        "Program Code": program_code,
                        "Semester Code": semester_code,
                        "Year": None,
                        "Course Classification": morning_slot_type,
                        "Course Code": course_code,
                        "Course Type": course_type,
                        "Faculty Code": sec["faculty_code"],
                        "Shift Timing": shift_timing,
                        "Slot Time": "09:30 TO 13:00",
                        "Section Code": sec["section"],
                        "Group": None,
                        "Academic Block": academic_block,
                        "Room Allocation": sec["room"],
                        "Combined Class": None,
                        "Mode of Class": "OFFLINE",
                        "Time Table Type": None
                    })
                    
                    # Slot 2: Afternoon Slot (Omitted on Thursday if half-day enabled)
                    if not (is_thursday and thursday_half_day):
                        rows.append({
                            "Date": date_str,
                            "Program Code": program_code,
                            "Semester Code": semester_code,
                            "Year": None,
                            "Course Classification": afternoon_slot_type,
                            "Course Code": course_code,
                            "Course Type": course_type,
                            "Faculty Code": sec["faculty_code"],
                            "Shift Timing": shift_timing,
                            "Slot Time": "13:55 TO 17:30",
                            "Section Code": sec["section"],
                            "Group": None,
                            "Academic Block": academic_block,
                            "Room Allocation": sec["room"],
                            "Combined Class": None,
                            "Mode of Class": "OFFLINE",
                            "Time Table Type": None
                        })
            cur_date += datetime.timedelta(days=1)
        
        df_result = pd.DataFrame(rows)
        st.success(f"Generated {len(df_result)} schedule rows successfully!")
        st.dataframe(df_result, use_container_width=True)
        
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df_result.to_excel(writer, sheet_name='Sheet1', index=False)
        
        st.download_button(
            label="📥 Download Timetable Excel (.xlsx)",
            data=buffer.getvalue(),
            file_name=f"UID_Timetable_{program_code}_Sem{semester_code}_{start_date}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
