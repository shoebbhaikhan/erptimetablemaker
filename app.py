import streamlit as st
import pandas as pd
import datetime
import io

st.set_page_config(page_title="UID Timetable Generator", layout="wide")

# ---------------------------------------------------------
# 1. MASTER COURSE & CURRICULUM CATALOG
# ---------------------------------------------------------
COURSES_DATA = [
    # 1st Sem B.Des (PSD) Batch 2026-30
    {"code": "26UDU01001", "title": "Design Essentials", "sem": "I", "prog_code": "1019", "batch": "1st Sem B.Des (PSD) 2026-30"},
    {"code": "26UDU01002", "title": "Visual Representation Skills", "sem": "I", "prog_code": "1019", "batch": "1st Sem B.Des (PSD) 2026-30"},
    {"code": "26UDU01103", "title": "Materials and Craftsmanship I", "sem": "I", "prog_code": "1019", "batch": "1st Sem B.Des (PSD) 2026-30"},
    {"code": "26UDU01204", "title": "Colour and Form", "sem": "I", "prog_code": "1019", "batch": "1st Sem B.Des (PSD) 2026-30"},
    {"code": "26UDU01305", "title": "History of Art & Design", "sem": "I", "prog_code": "1019", "batch": "1st Sem B.Des (PSD) 2026-30"},
    {"code": "26UDU01406", "title": "Fundamentals of AI", "sem": "I", "prog_code": "1019", "batch": "1st Sem B.Des (PSD) 2026-30"},
    {"code": "26UDU01607", "title": "Digital Tools", "sem": "I", "prog_code": "1019", "batch": "1st Sem B.Des (PSD) 2026-30"},
    
    # 3rd Sem B.Des Product Design Batch 2025-29
    {"code": "UC012030001", "title": "Personality Development", "sem": "III", "prog_code": "1019", "batch": "3rd Sem B.Des PD 2025-29"},
    {"code": "31203001203", "title": "Design Research", "sem": "III", "prog_code": "1019", "batch": "3rd Sem B.Des PD 2025-29"},
    {"code": "31203006211", "title": "Product Visualization", "sem": "III", "prog_code": "1019", "batch": "3rd Sem B.Des PD 2025-29"},
    {"code": "31203006212", "title": "Form, Aesthetic and Emotion", "sem": "III", "prog_code": "1019", "batch": "3rd Sem B.Des PD 2025-29"},
    {"code": "31203006207", "title": "Studio- Human Centric Design", "sem": "III", "prog_code": "1019", "batch": "3rd Sem B.Des PD 2025-29"},
    {"code": "31203006215", "title": "Design Articulation with AI", "sem": "III", "prog_code": "1019", "batch": "3rd Sem B.Des PD 2025-29"},
    {"code": "31203006214", "title": "Indian Design System", "sem": "III", "prog_code": "1019", "batch": "3rd Sem B.Des PD 2025-29"},
    
    # 5th Sem B.Des Product Design Batch 2024-28
    {"code": "31305006328", "title": "CAID", "sem": "V", "prog_code": "1019", "batch": "5th Sem B.Des PD 2024-28"},
    {"code": "31305001303", "title": "Conceptualization & Characterization", "sem": "V", "prog_code": "1019", "batch": "5th Sem B.Des PD 2024-28"},
    {"code": "31305001304", "title": "Speed Modelling in Clay", "sem": "V", "prog_code": "1019", "batch": "5th Sem B.Des PD 2024-28"},
    {"code": "31305001306", "title": "Space Perception", "sem": "V", "prog_code": "1019", "batch": "5th Sem B.Des PD 2024-28"},
    {"code": "31305001324", "title": "Matte-Painting", "sem": "V", "prog_code": "1019", "batch": "5th Sem B.Des PD 2024-28"},
    {"code": "31305001325", "title": "Ad Film Production", "sem": "V", "prog_code": "1019", "batch": "5th Sem B.Des PD 2024-28"},
    {"code": "31305001326", "title": "Fashion Styling", "sem": "V", "prog_code": "1019", "batch": "5th Sem B.Des PD 2024-28"},
    {"code": "31305001327", "title": "UX/UI", "sem": "V", "prog_code": "1019", "batch": "5th Sem B.Des PD 2024-28"},
    {"code": "31305001328", "title": "The Art of Delightful Design", "sem": "V", "prog_code": "1019", "batch": "5th Sem B.Des PD 2024-28"},
    {"code": "31305001329", "title": "Branding And Identity Design", "sem": "V", "prog_code": "1019", "batch": "5th Sem B.Des PD 2024-28"},
    {"code": "31305006322", "title": "Human Factors", "sem": "V", "prog_code": "1019", "batch": "5th Sem B.Des PD 2024-28"},
    {"code": "31305006329", "title": "Portfolio Design with Voice Agents", "sem": "V", "prog_code": "1019", "batch": "5th Sem B.Des PD 2024-28"},
    {"code": "31305006324", "title": "Studio- Humanizing Technology", "sem": "V", "prog_code": "1019", "batch": "5th Sem B.Des PD 2024-28"},
    {"code": "31305006325", "title": "Experience Design", "sem": "V", "prog_code": "1019", "batch": "5th Sem B.Des PD 2024-28"},
    {"code": "31305006326", "title": "Packaging Design", "sem": "V", "prog_code": "1019", "batch": "5th Sem B.Des PD 2024-28"},
    {"code": "31305006327", "title": "Speculative design", "sem": "V", "prog_code": "1019", "batch": "5th Sem B.Des PD 2024-28"},
    
    # 7th Sem B.Des Product Design Batch 2023-27
    {"code": "31407001400", "title": "Design Management", "sem": "VII", "prog_code": "1019", "batch": "7th Sem B.Des PD 2023-27"},
    {"code": "31407006403", "title": "Internship", "sem": "VII", "prog_code": "1019", "batch": "7th Sem B.Des PD 2023-27"},
    {"code": "31407006405", "title": "System Analysis and Design with Voice Agents", "sem": "VII", "prog_code": "1019", "batch": "7th Sem B.Des PD 2023-27"},
    
    # 1st Sem M.Des Product & Service Design Batch 2026-28
    {"code": "26UDP01317", "title": "Design Appreciation & Storytelling", "sem": "I", "prog_code": "1025", "batch": "1st Sem M.Des PSD 2026-28"},
    {"code": "26UDP01018", "title": "Design Foundation", "sem": "I", "prog_code": "1025", "batch": "1st Sem M.Des PSD 2026-28"},
    {"code": "26UDP01019", "title": "Form Studies", "sem": "I", "prog_code": "1025", "batch": "1st Sem M.Des PSD 2026-28"},
    {"code": "26UDP01020", "title": "Design Studio I", "sem": "I", "prog_code": "1025", "batch": "1st Sem M.Des PSD 2026-28"},
    {"code": "26UDP01421", "title": "Design Prototyping", "sem": "I", "prog_code": "1025", "batch": "1st Sem M.Des PSD 2026-28"},
    {"code": "26UDP01122", "title": "Frugal Innovation", "sem": "I", "prog_code": "1025", "batch": "1st Sem M.Des PSD 2026-28"},
    {"code": "26UDP01123", "title": "Emergent Technology", "sem": "I", "prog_code": "1025", "batch": "1st Sem M.Des PSD 2026-28"},
    {"code": "26UDP01624", "title": "CAID", "sem": "I", "prog_code": "1025", "batch": "1st Sem M.Des PSD 2026-28"},
    
    # 3rd Sem Masters in Industrial Design Batch 2025-27
    {"code": "32203001602", "title": "Internship", "sem": "III", "prog_code": "1025", "batch": "3rd Sem M.Des ID 2025-27"},
    {"code": "32203001603", "title": "Entrepreneurship", "sem": "III", "prog_code": "1025", "batch": "3rd Sem M.Des ID 2025-27"},
    {"code": "32203001604", "title": "Research Methodology", "sem": "III", "prog_code": "1025", "batch": "3rd Sem M.Des ID 2025-27"},
    {"code": "32203002613", "title": "Generative AI for UI & UX Design", "sem": "III", "prog_code": "1025", "batch": "3rd Sem M.Des ID 2025-27"},
    {"code": "32203002610", "title": "Studio: Design and Technology", "sem": "III", "prog_code": "1025", "batch": "3rd Sem M.Des ID 2025-27"},
    {"code": "32203002611", "title": "Lighting Design", "sem": "III", "prog_code": "1025", "batch": "3rd Sem M.Des ID 2025-27"},
    {"code": "32203002612", "title": "Craft and Technology", "sem": "III", "prog_code": "1025", "batch": "3rd Sem M.Des ID 2025-27"},
]

# Build dropdown mapping options
COURSE_OPTIONS = {
    f"{c['title']}  |  [{c['code']}]  ({c['batch']})": c for c in COURSES_DATA
}
COURSE_OPTIONS["✏️ [Custom / Manual Course Entry]"] = {
    "code": "", "title": "Custom", "sem": "I", "prog_code": "1019", "batch": "Custom"
}

# ---------------------------------------------------------
# 2. UID FACULTY MASTER DIRECTORY
# ---------------------------------------------------------
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

SEMESTERS = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII"]
DAYS_MAP = {"Mon": 0, "Tue": 1, "Wed": 2, "Thu": 3, "Fri": 4, "Sat": 5}

# ---------------------------------------------------------
# UI SETUP
# ---------------------------------------------------------
st.title("UID Timetable Auto-Population Tool")
st.caption("Search Course Title/Code to auto-fetch semester details, configure sections, and export structured timetable schedules.")

col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.subheader("1. Course & Curriculum Selection")
    
    selected_course_key = st.selectbox(
        "Search Course Name or Course Code:",
        options=list(COURSE_OPTIONS.keys()),
        index=0
    )
    
    course_info = COURSE_OPTIONS[selected_course_key]
    
    # Dynamic or Manual Fields
    if selected_course_key == "✏️ [Custom / Manual Course Entry]":
        c_code_col, c_type_col = st.columns(2)
        course_code = c_code_col.text_input("Enter Course Code", value="")
        course_type = c_type_col.selectbox("Course Type", ["MANDATORY", "ELECTIVE"], index=0)
        
        cp1, cp2 = st.columns(2)
        program_code = cp1.text_input("Program Code", value="1019")
        semester_code = cp2.selectbox("Semester Code", SEMESTERS, index=0)
    else:
        course_code = course_info["code"]
        default_sem_idx = SEMESTERS.index(course_info["sem"]) if course_info["sem"] in SEMESTERS else 0
        
        c_type_col, c_sem_col, c_prog_col = st.columns([1.5, 1, 1])
        course_type = c_type_col.selectbox("Course Type", ["MANDATORY", "ELECTIVE"], index=0)
        semester_code = c_sem_col.selectbox("Semester Code", SEMESTERS, index=default_sem_idx)
        program_code = c_prog_col.text_input("Program Code", value=course_info["prog_code"])
        
        st.info(f"📌 Auto-Fetched: **Code:** `{course_code}` | **Sem:** `{semester_code}` | **Prog:** `{program_code}`")

    st.subheader("2. Schedule & Slot Timings")
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
    
    c_slot1, c_slot2, c_blk = st.columns([1.5, 1.5, 1])
    morning_slot_type = c_slot1.selectbox("Morning Slot", ["THEORY", "PRACTICAL"], index=0)
    afternoon_slot_type = c_slot2.selectbox("Afternoon Slot", ["PRACTICAL", "THEORY"], index=0)
    academic_block = c_blk.text_input("Academic Block", value="F")

with col_right:
    st.subheader("3. Dynamic Section Allocations")
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
            fac_code = s_col1.text_input(f"Type Faculty Code (Sec {sec})", key=f"fac_custom_{sec}")
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
        st.error("Please enter or select a valid Course Code.")
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
                    # Morning Slot
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
                    
                    # Afternoon Slot (Skipped on Thursday if toggle active)
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
        
        # Excel Export Buffer
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df_result.to_excel(writer, sheet_name='Sheet1', index=False)
        
        st.download_button(
            label="📥 Download Timetable Excel (.xlsx)",
            data=buffer.getvalue(),
            file_name=f"UID_Timetable_{program_code}_Sem{semester_code}_{start_date}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
