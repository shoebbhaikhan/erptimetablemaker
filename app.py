import streamlit as st
import pandas as pd
import datetime
import io

st.set_page_config(page_title="UID Timetable Generator", layout="wide")

# ---------------------------------------------------------
# MASTER LOOKUP DATA (UID Only)
# ---------------------------------------------------------
UID_PROGRAMS = {
    "B.Design (Hons.) Product Design": "1019",
    "M.Design (Industrial Design)": "1025",
    "B.Design (Hons.) Interaction Design": "1015",
    "B.Design (Hons.) Automobile and Transportation Design": "1006",
    "B.Design (Hons.) Interior & Furniture Design": "1016",
    "B.Design (Hons.) Visual Communication": "1007",
    "B.Design (Hons.) Animation & Digital Media": "1003",
    "B.Design (Hons.) Fashion Design": "1009",
    "Foundation / Interdisciplinary (UG)": "1116",
}

COURSE_CATALOG = {
    "Design Project 3 (31305006324)": {"code": "31305006324", "type": "MANDATORY"},
    "Advanced Modeling (31305006329)": {"code": "31305006329", "type": "MANDATORY"},
    "Design Fundamentals (26UDP01020)": {"code": "26UDP01020", "type": "MANDATORY"},
    "Industry Project (32203002610)": {"code": "32203002610", "type": "MANDATORY"},
    "Custom / Manual Entry": {"code": "", "type": "MANDATORY"}
}

SEMESTERS = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII"]
DAYS_MAP = {"Mon": 0, "Tue": 1, "Wed": 2, "Thu": 3, "Fri": 4, "Sat": 5}

# ---------------------------------------------------------
# UI LAYOUT
# ---------------------------------------------------------
st.title("UID Timetable Auto-Population Tool")
st.caption("Generate institutional timetable schedules without redundant data entry.")

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
    
    # Thursday Half-Day Checkbox
    thursday_half_day = st.checkbox("Thursday Afternoon Off (Half Day)", value=True)
    
    c_p1, c_p2 = st.columns(2)
    prog_name = c_p1.selectbox("UID Program", list(UID_PROGRAMS.keys()))
    program_code = UID_PROGRAMS[prog_name]
    semester_code = c_p2.selectbox("Semester", SEMESTERS, index=4)
    
    st.subheader("2. Course & Slot Details")
    course_name = st.selectbox("Course / Subject", list(COURSE_CATALOG.keys()))
    
    if course_name == "Custom / Manual Entry":
        c_code_col, c_type_col = st.columns(2)
        course_code = c_code_col.text_input("Enter Course Code", value="")
        course_type = c_type_col.text_input("Course Type", value="MANDATORY")
    else:
        course_code = COURSE_CATALOG[course_name]["code"]
        course_type = COURSE_CATALOG[course_name]["type"]
        st.info(f"Course Code: **{course_code}** | Type: **{course_type}**")

    c_slot1, c_slot2 = st.columns(2)
    morning_slot_type = c_slot1.selectbox("Morning Slot (09:30 - 13:00)", ["THEORY", "PRACTICAL"], index=0)
    afternoon_slot_type = c_slot2.selectbox("Afternoon Slot (13:55 - 17:30)", ["PRACTICAL", "THEORY"], index=0)
    academic_block = st.text_input("Academic Block", value="F")

with col_right:
    st.subheader("3. Dynamic Section Allocations")
    num_sections = st.slider("Number of Sections in Batch", min_value=1, max_value=5, value=4)
    
    section_labels = ["A", "B", "C", "D", "E"][:num_sections]
    section_inputs = []
    
    st.write("Assign Faculty and Room per Section:")
    for sec in section_labels:
        s_col1, s_col2, s_col3 = st.columns([1, 2, 2])
        s_col1.markdown(f"### Sec {sec}")
        fac = s_col2.text_input(f"Faculty Code (Sec {sec})", key=f"fac_{sec}")
        room = s_col3.text_input(f"Room Allocation (Sec {sec})", key=f"room_{sec}")
        section_inputs.append({
            "section": sec,
            "faculty_code": fac.strip(),
            "room": room.strip()
        })

# ---------------------------------------------------------
# GENERATION ENGINE
# ---------------------------------------------------------
st.markdown("---")

if st.button("Generate Timetable", type="primary"):
    missing = [s['section'] for s in section_inputs if not s['faculty_code'] or not s['room']]
    if missing:
        st.error(f"Missing Faculty Code or Room for Section(s): {', '.join(missing)}")
    elif not course_code:
        st.error("Please enter a valid Course Code.")
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
                    # Slot 1 (Morning - Always Created)
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
                    
                    # Slot 2 (Afternoon - Skipped on Thursday if box is checked)
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