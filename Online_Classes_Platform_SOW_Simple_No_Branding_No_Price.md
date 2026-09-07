# **Statement of Work — Online Classes Platform** 

Simple Version — Branding and Commercial Information Removed 

Document Control 

Project Online Classes Platform 

Prepared for Client / Academy Name 

Prepared by 

Scope source Online-Classes-Platform-Requirements-v1, prepared after the meeting of 23 July 2026 

## **1. Project Overview** 

The Online Classes Platform is a private, Zoom-style class environment for an academy. Each teacher has a permanent meeting ID and link. Students join at class time from the web or mobile app, the teacher controls admission, and every valid class is recorded automatically into the administrator's recording library. The platform restricts direct teacher-to-student messaging and uses AI to review recordings, produce class-level feedback, track improvement, and provide an academywide teacher performance view. 

Class scheduling and recurring meeting management remain in the client's existing ERP. This project does not replace the ERP, payment system, or learning management functions. 

## **2. Project Vision and Objectives** 

The objective is to give the academy a controlled online classroom system that protects student relationships, centralizes class recordings, and gives management clear, current visibility into teaching quality. 

## **1. Provide frictionless class access** 

Students join through a permanent teacher meeting ID or link on web, Android, or iOS. 

## **2. Protect academy communication boundaries** 

Students have no chat anywhere on the platform, and teachers can chat only with administrators. 

## **3. Create a complete recording trail** 

Every class is automatically recorded and stored with teacher, student, date, time, and duration 

metadata. 

## **4. Improve teacher quality with AI** 

Valid recordings are analyzed automatically to generate class feedback, improvement suggestions, progress tracking, grades, and rankings. 

## **5. Support central academy oversight** 

Administrators manage all accounts, meeting IDs, recordings, live sessions, teacher communications, and performance results from one portal. 

## **3. Scope of Work** 

### **3.1 Platform Model** 

- The solution will be a private academy platform, not a public meeting service. 

- Each teacher will have one permanent meeting ID and shareable link. The administrator may retain 

- or change that ID at any time. 

- Students may enter the meeting ID or open the link to join from the web or mobile app. 

- The platform will not create or manage class schedules or recurring meetings. Scheduling 

remains in the existing ERP. 

- When a participant joins, the teacher can admit or remove that participant. 

### **3.2 Accounts and Roles** 

Role Account control Primary capabilities Communicationrights 

Administrator 

Creates, edits, deactivates, 

and manages all accounts 

Manages meeting IDs, 

users, recordings, active sessions, AI grades, rankings, and teacher 

chat 

Can chat with teachers; 

no student chat channel is required 

Teacher 

Uses an individual login 

created by the administrator 

Hosts classes, 

admits/removes 

participants, shares screen, 

reviews class records and 

AI feedback 

Can chat with 

administrators only 

Student 

Uses an individual login created by the administrator Joins a teacher meeting through ID/link,controls own microphone, and raises hand 

No chat anywhere on the 

platform 

### **3.3 In-Class Experience** 

- HD video and audio with one-tap joining.Teacher and student can mute or unmute their own microphone. 

- Student can raise a hand to get the teacher's attention. 

- Teacher can admit or remove participants at any time. 

- Teacher can share the screen for lesson material. 

- No in-class chat will be available. 

- The teacher cannot stop or pause automatic recording. 

Scheduling clarification 

The platform does not create future schedules. The weekly and monthly teacher view will show 

sessions recognized by the platform, such as completed or recorded classes. Displaying future ERP 

schedules requires a later ERP integration or another agreed data source. 

### **3.4 Recording and Media Library** 

- Every class will be recorded automatically. 

- All recordings will be stored in the administrator's library with teacher, student, date, time, and 

duration metadata. 

- The recording library will be searchable by teacher, student, date, and time. 

- Recordings below an agreed minimum file size or duration will be skipped by the AI process so 

short or empty sessions are ignored. 

• The source requirement states that no recording indicator is shown during the class. This is subject to the legal consent and disclosure clause in Section 12.10; mandatory legal or platform disclosures take precedence. 

### **3.5 Administrator Portal** 

- Create, edit, deactivate, and search teacher and student accounts. 

- Set or change any teacher's permanent meeting ID. 

- Access the complete searchable recording library. 

- View a live sessions wall showing all currently active classes and the participant count in each 

- session. 

- View teacher grades A, B, C, or D, Teacher of the Month, and the top-three ranking. 

- Open a direct chat channel with each teacher. 

- View AI analysis status and results linked to the correct teacher, student, and recording. 

- Access audit information for sensitive administrative actions. 

### **3.6 Teacher Portal** 

- View class records for the current week and month, with links to each class record and its 

- recording. 

- View AI analysis for every valid class recording. 

- View personal improvement suggestions and a history of progress achieved against those 

suggestions. 

- Chat with the administrator only, including operational messages such as reporting that a 

student has not joined. 

- Access the permanent meeting ID and link assigned by the administrator. 

### **3.7 Student Portal** 

- Authenticate with an individual student account created by the administrator. 

- Enter a meeting ID or open a shared teacher link to join the class from web or mobile. 

- Use class controls permitted to students: own microphone mute/unmute and raise hand. 

- No student chat, teacher messaging, payment, fee management, homework, lesson 

management, or student progress module is included. 

### **3.8 Communication Policy** 

- Students will have no chat anywhere on the platform. 

- Teacher-to-student chat will not be possible inside or outside the class. 

- The only chat channel on the platform will be Teacher <-> Administrator. 

- Role permissions and API access controls will enforce these restrictions. 

### **3.9 AI Analysis and Teacher Grading** 

- An automated worker will check for new recordings every 30 minutes. 

- Recordings below the agreed minimum size or duration will be skipped. 

- Every valid recording will be analyzed automatically. 

- Each teacher will receive per-class analysis, improvement suggestions, and progress tracking 

- against those suggestions. 

- The administrator will receive current A/B/C/D grades, Teacher of the Month, and top-three 

- performance rankings. 

- AI grades and recommendations are advisory. Human review is required before using them for 

- employment, discipline, compensation, or any other decision materially affecting a teacher. 

### **3.10 Supported Platforms** 

- Responsive web portal for administrator, teacher, and student roles. 

- Android mobile application for joining classes and accessing the permitted portal functions. 

- iOS mobile application for joining classes and accessing the permitted portal functions. 

## **4. Detailed Functional Requirements** 

FR-001 - Administrator account management: The administrator shall create, edit, deactivate, and 

search all teacher and student accounts. 

FR-002 - Individual authentication: Each teacher and student shall sign in with an individual account so sessions, recordings, and AI analysis are linked to the correct users. 

FR-003 - Permanent teacher meeting ID: Each teacher shall have one permanent meeting ID and link. 

FR-004 - Meeting ID administration: The administrator shall be able to change or retain any teacher 

meeting ID. 

FR-005 - Link sharing: The teacher meeting link may be shared through WhatsApp or any other external channel. 

FR-006 - Join by ID or link: A student shall join by entering the meeting ID or opening the link from web, Android, or iOS. 

FR-007 - No internal scheduling: The platform shall not create class schedules or recurring meetings. FR-008 - Teacher admission control: The teacher shall admit or remove joining participants. 

FR-009 - Audio and video: The class shall provide HD audio and video subject to participant network and device capability. 

FR-010 - Self microphone control: Teachers and students shall mute or unmute their own microphone. FR-011 - Raise hand: Students shall be able to raise a hand. 

FR-012 - Screen sharing: Teachers shall be able to share their screen. 

FR-013 - No class chat: No chat feature shall be present inside a class. 

FR-014 - Automatic recording: Every class shall start recording automatically. 

FR-015 - Recording control restriction: Teachers shall not be able to pause or stop the recording. 

FR-016 - Recording indicator behavior: The class interface shall not display an in-session recording indicator as requested, except where applicable law, third-party platform rules, or approved compliance design requires a disclosure. 

FR-017 - Recording metadata: Each recording shall store teacher, student, date, time, and 

duration metadata. 

FR-018 - Recording library search: The administrator shall search recordings by teacher, student, date, and time. 

FR-019 - Live sessions wall: The administrator shall see all active classes and the participant count for each. 

FR-020 - Teacher-admin chat: The platform shall provide direct chat between each teacher and the administrator. 

FR-021 - Student communication restriction: Students shall have no chat channel and shall not 

message teachers or administrators through the platform. 

FR-022 - Teacher class history: Teachers shall see class records for the current week and month with recording links. 

FR-023 - Recording scan interval: The AI worker shall check for new recordings every 30 minutes. 

FR-024 - Trivial recording filter: The AI worker shall skip recordings below the client-approved minimum size or duration. 

FR-025 - Per-class analysis: Each valid recording shall produce a class-level AI analysis. 

FR-026 - Improvement suggestions: Each analysis shall include actionable improvement points for the teacher. 

FR-027 - Progress tracking: The system shall track change over time against previously issued improvement points. 

FR-028 - Teacher grades: The administrator shall see current A/B/C/D teacher grades based on the approved grading rubric. 

FR-029 - Recognition and ranking: The administrator shall see Teacher of the Month and the topthree ranking. 

FR-030 - Human oversight: AI outputs shall remain reviewable by the administrator and shall not be the sole basis for material employment decisions. 

FR-031 - Cross-platform access: The agreed functions shall be available through the responsive web portal and mobile apps according to role. 

FR-032 - Auditability: Sensitive administrative changes, recording processing events, and AI analysis status shall be logged for operational traceability. 

## **5. Project Deliverables** 

ID Deliverable Description 

D1 Responsive Web Application 

Role-based web portal for 

administrators, teachers, and students. 

D2 Android Application Android app for class joining and 

role-permitted portal access. 

D3 iOS Application iOS app for class joining and role- 

permitted portal access. 

D4 Real-Time Classroom Module Permanent meeting IDs, join flow, admission control, HD audio/video, 

microphone controls, hand raise, and 

teacher screen sharing. 

D5 Automatic Recording Pipeline 

Uninterruptible class recording, 

recording metadata, storage workflow, and recording availability status. 

D6 Administrator Portal 

User management, meeting ID management, recording search, live sessions wall, teacher chat, and performance overview. 

D7 Teacher Portal 

Class history, recording links, AI analysis, improvement suggestions, progress tracking, and administrator chat. ID Deliverable Description D8 Student Access Experience Secure login and class joining without any messaging, 

scheduling, payment, or LMS 

features. 

D9 AI Analysis and Grading Engine 30-minute recording discovery process, recording filters, perclass analysis, improvement tracking, grades, Teacher of the Month, and top-three ranking. D10 Security and Audit Controls Role enforcement, communication restrictions,secure authentication, operational logs, and administrative audit records. D11 Deployment Package Configured production environments, deployment files, environment documentation, and handover instructions. D12 Source Code and Documentation 

Project-specific source code, technical documentation, setup instructions, and administrator operating guide, subject to payment and license terms. 

## **6. Non-Functional and Technical** 

Requirements 

### **6.1 Security and Access Control** 

- Role-based authorization shall prevent users from accessing functions or data outside their role. 

- Authentication credentials, tokens, and administrative actions shall be handled through secure 

application practices. 

- Data in transit shall use encrypted connections. Stored recordings and personal data shall use 

- access-controlled storage. 

- Administrative and AI processing actions shall be traceable through logs. 

### **6.2 Reliability and Processing** 

- Automatic recording and AI processing shall include retry handling and visible processing status for 

- failed or delayed jobs. 

- The AI worker shall run at least every 30 minutes, subject to the agreed hosting design and 

service availability. 

- Recording metadata shall remain linked to the correct teacher, student, and class record. 

### **6.3 Performance and Scale** 

- The final infrastructure size, participant limits, recording throughput, and simultaneous class 

capacity shall be based on the client-confirmed teacher count and peak concurrency. 

- Video quality depends on end-user bandwidth, device capability, and the selected real-time 

- communications provider. 

- The system shall support horizontal expansion where the selected hosting and video provider 

- permit it. 

### **6.4 Privacy, Recording, and AI Governance** 

- The client shall define the recording retention period, download permissions, and authorized 

viewers before production launch. 

- All required notices and consents for recording, transcription, and AI analysis must be obtained and 

- documented. 

- AI results shall be treated as advisory and subject to human validation. 

### **6.5 Cross-Platform Quality** 

- The web experience shall be responsive for supported desktop and mobile browsers. 

- Android and iOS builds shall follow the approved platform versions and app-store requirements. 

- Core class controls and role restrictions shall behave consistently across supported platforms. 

## **7. AcceptanceCriteria** 

## **1. Administrator can create, edit, deactivate, and search teacher and student accounts.** 

## **2. Administrator can assign and change a permanent meeting ID for each teacher.** 

## **3. Student can join a teacher class by meeting ID or link from the supported web and mobile** 

applications. 

## **4. Teacher can admit or remove participants, share screen, and use the permitted class controls.** 

## **5. Student can mute/unmute their microphone and raise a hand, but cannot access any chat.** 

## **6. Teacher cannot pause or stop automatic recording.** 

## **7. Completed class recordings appear in the administrator library with the required metadata and can** 

be searched by teacher, student, date, and time. 

## **8. Administrator can view all active sessions and the participant count for each.** 

## **9. Teacher can view current week and month class records, recording links, AI analysis,** 

suggestions, and progress history. 

## **10. Teacher and administrator can exchange messages; no teacher-student or student-admin chat is** 

available. 

## **11. The AI worker detects new recordings on the agreed 30-minute cycle, skips trivial recordings** 

according to the approved threshold, and produces analysis for valid recordings. 

## **12. Administrator can view A/B/C/D grades, Teacher of the Month, and the top-three ranking after the** 

grading rubric is approved. 

## **13. Role permissions, recording consent controls, audit logs, and human review requirements pass UAT.** 

## **14. Project-specific documentation and handover materials are delivered.** 

The project will be considered functionally accepted when these criteria have passed written 

client UAT and all agreed critical defects have been resolved or formally accepted as deferred. 

## **8. Not Included in This Phase** 

- Class scheduling and recurring meeting management. These remain in the client's ERP. 

- Payments, fee collection, billing, and finance management. 

- Student learning management, including lessons, homework, assessments, and student 

academic progress tracking. 

- ERP integration. It may be scoped as a later phase. 

- Teacher-to-student or student-to-administrator chat. 

- Any feature, integration, report, language, scale target, recording retention policy, or download 

permission not stated in this SOW or later approved through change control. 

## **9. Configuration Decisions Required Before Final** 

Build and Production Sizing 

Decision Confirmation required 

Class size 

Will a class always be one teacher with one student, or 

may several students join the same teacher session? 

Recording segmentation 

When classes run back-to-back on the same meeting 

ID, should each student class be saved as a separate 

recording? The source document recommends yes. 

AI skip threshold What minimum recording file size or duration should be 

#### ignored as trivial? 

#### Decision Confirmation required 

AI language Should analysis and suggestions be written in English, 

Urdu, or both? 

Live captions Are live captions or subtitles required during class? 

Recording access Will recordings be downloadable or view-only, and which 

roles may access them? 

System scale How many teachers exist, and how many classes run 

simultaneously at peak hours? 

Recording retention How long must recordings, transcripts, and AI results be 

retained? 

Grading rubric What criteria and weightsdefine A/B/C/D, Teacherof the 

Month, and the top-three ranking? 

Recording disclosures What approved notice and consent process will the 

academy use for students, guardians, and teachers? 

Effect of unresolved decisions 

These decisions may affect the schedule, final architecture, cloud estimate, mobile release plan, and AI rubric. Any change to the agreed scope or fee requires written change control and client approval. 

## **10. Client Responsibilities** 

- Confirm the open configuration decisions and approve the final requirements in writing. 

- Provide brand assets, user lists, test accounts, policy text, grading rubric, and representative class 

- recordings where legally permitted. 

- Provide or fund required third-party accounts, cloud services, video/RTC services, storage, AI services, 

- app-store accounts, certificates, and licenses unless they are expressly included in the 

project budget or otherwise agreed in writing. 

- Obtain all required notices, permissions, guardian approvals, and consents for recording, 

monitoring, transcription, and AI analysis. 

- Provide timely access to client personnel, systems, and test users needed for discovery, UAT, and 

- launch. 

- Review deliverables and provide consolidated written feedback within the response periods in 

- Section 12. 

- Use the platform in accordance with the Acceptable Use provisions set out below. 

## **11. Responsibilities** 

- Design and implement the agreed web, Android, iOS, RTC, recording, administration, chat, and AI 

functions stated in this SOW. 

- Apply role restrictions so student communication is blocked and teacher chat is limited to 

administrators. 

- Configure reasonable security controls, error handling, monitoring, audit logging, and 

deployment documentation for the agreed architecture. 

- Run internal testing and support client UAT against the acceptance criteria. 

- Deliver project-specific source code and documentation according to the payment and 

ownership terms. 

- Identify material scope gaps, legal-compliance conflicts, third-party limitations, or scaling 

constraints when they become known. 

- Process suspected acceptable-use violations in accordance with the Enforcement section below. 

## **12. Contract Terms and Conditions** 

### **12.1 Change Requests** 

- Minor cosmetic changes may be completed without additional charge when 

determines that they do not affect architecture, testing, delivery effort, or schedule. 

- A change that affects scope, system behavior, integrations, security, data model, performance, 

- schedule, or regression testing will follow the change-control process. 

- will document the requested change, reason, impact, estimated additional effort, 

- pricing, and schedule effect. 

- Changes too large for the current development cycle may be proposed as a separate phase. 

- Change effort normally increases after implementation is substantially underway because 

- existing functions must be regression-tested. 

- Approved change-request charges will be invoiced separately and must be paid before the 

- changed functionality is released to production. 

### **12.2 Change-Control Procedure** 

- Either party may initiate a Project Change Request (PCR). 

- The PCR will describe the change, reasons, and effect on scope, price, schedule, resources, and 

- contractual commitments. 

- The designated contacts will review, approve, reject, or request investigation of the PCR. 

- Any charge for impact investigation will be disclosed before the investigation begins. 

- No change becomes binding until both parties approve it in writing. 

- After approval, the SOW, cost, schedule, and relevant commercial documents will be updated, and 

- the PCR reference will be used for invoicing. 

### **12.3 Completion and Acceptance** 

- The project is complete when the deliverables and acceptance criteria in this SOW have been 

fulfilled and delivered to the client. 

- The client will test the delivered functionality and provide written acceptance or a consolidated 

- defect list. 

- Defects are issues where delivered functionality does not materially conform to this SOW. New 

- functionality, preference changes, and requirements not stated here are change requests. 

- If the SOW must be amended, will use the change-control procedure in Section 12.2. 

### **12.4 Engagement-Related Expenses and Third-Party Costs** 

• The client will bear all approved third-party expenses required for the solution that are not expressly included in the agreed scope, including cloud hosting, RTC/video services, storage, AI APIs, app-store fees, certificates, special hardware, paid templates, and licenses. 

- is not required to absorb third-party tools, servers, commercial libraries, or license costs 

- unless they are expressly included in the agreed scope or separately agreed in writing. 

• All amounts due must be paid before production go-live or app-store submission. 

- No contingency amount is included in the project budget. Any unforeseen work outside the 

- agreed scope requires a written and approved change request before additional charges apply. 

- Invoices will be issued according to the two payment milestones in Section 12.7. Wire details will 

- appear on each invoice. 

### **12.5 Intellectual Property** 

- Unless otherwise agreed in writing, the client will own the project-specific deliverables after full 

- payment. 

- Open-source, third-party, and commercially licensed components remain subject to their 

- respective licenses and are not transferred beyond the rights granted by those licenses. 

- Ownership transfer does not apply to unpaid deliverables or to services, licenses, infrastructure, or 

- components owned by third parties. 

### **12.6 Warranty, Maintenance, and Upgrades** 

- will provide a one-month warranty for minor bug fixes and reasonable support for the 

- delivered scope. 

• The warranty does not include change requests, new features, new integrations, new platform requirements, third-party service changes, misuse, or issues caused by client or third-party modifications. 

- Long-term maintenance or service-level commitments require a separate maintenance or SLA 

- document. 

- Future upgrades or new requirements require a separate SOW or approved change request with 

- impact analysis and regression-testing scope. 

### **12.8 Communication, Feedback, and Client Delay** 

- Both parties should respond to project questions within 24 hours where reasonably possible. 

- If required client feedback or access is not provided within 24-48 hours, may place the 

- project on hold and move it behind other scheduled work. 

• Resuming after an unreasonable delay may incur a restart fee of at least $500 for a project for this project. Larger projects may incur a higher restart fee based on the losses and remobilization effort assessed by . 

• Feedback must be provided in writing, promptly, and in a consolidated form. Late or incomplete feedback may delay delivery and may require to proceed using reasonable implementation judgment. 

- Where consultancy is provided to discover or refine unclear requirements, the client should record 

and confirm meeting decisions as soon as possible. Once features and flows are locked after discovery, later changes are treated as change requests. 

- Customer training, custom manuals, workshops, or special data-export assistance not included in the 

- deliverables may be handled through a separate deliverable or change request. 

### **12.9 Suspension for Misuse or Security Risk** 

may investigate suspected misuse and may restrict or suspend affected access where reasonably necessary to protect users, systems, data, legal compliance, or service integrity. Enforcement is governed in more detail by the Acceptable Use provisions set out below. 

### **12.10 Recording, Monitoring, AI, and Legal Compliance** 

• The client is responsible for determining and complying with all laws, regulations, contracts, academy policies, and consent requirements that apply to class recording, monitoring, transcription, storage, AI analysis, and teacher performance review. 

- The client must provide required notices and obtain required consent from teachers, students, 

- parents, guardians, or other participants before use. 

• The requested absence of an in-session recording indicator does not remove the client's legal obligations. If a disclosure, indicator, audible notice, or consent control is required, the compliant implementation will override the no-indicator preference. 

• AI grades, rankings, and suggestions are decision-support outputs. The client must provide human review and must not use the AI result as the sole basis for a materially adverse employment or access decision. 

- Personal data and recordings must be handled under the applicable privacy documentation, 

- retention rules, and Data Processing Agreement where required. 

### **12.11 Governing Commercial Documents** 

This SOW defines the functional scope, finalized project budget, and payment milestones. Entity details, governing law, liability limits, confidentiality, data processing, and any service levels may also be governed by a signed Order Form, master services agreement, data processing agreement, and incorporated policies. Where documents conflict, the signed governing commercial document will control to the extent stated in that document. 

