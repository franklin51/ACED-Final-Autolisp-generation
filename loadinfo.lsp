(defun C:PRINTDXF ( )
  (setq ent (entlast))               ; Set ent to last entity.
  (setq entl (entget ent))           ; Set entl to association list of last entity.
  (setq ct 0)                        ; Set ct (a counter) to 0.
  (textpage)                         ; Switch to the text screen.
  (princ "\nentget of last entity:")
  (repeat (length entl)              ; Repeat for number of members in list:
    (print (nth ct entl))            ; Output a newline, then each list member.
    (setq ct (1+ ct))                ; Increments the counter by one.
  )
  
 (princ)                             ; Exit quietly.
)

(defun C:PRINT_Select_DXF ( )
  (setq ent_sel (entsel "select entity to get info"))               ; Set ent to last entity.
  (setq ent (car ent_sel))
  (setq entl (entget ent))           ; Set entl to association list of last entity.
  (setq ct 0)                        ; Set ct (a counter) to 0.
  (textpage)                         ; Switch to the text screen.
  (princ "\nentget of last entity:")
  (repeat (length entl)              ; Repeat for number of members in list:
    (print (nth ct entl))            ; Output a newline, then each list member.
    (setq ct (1+ ct))                ; Increments the counter by one.
  )
 (princ)                             ; Exit quietly.
)

(defun print_enetity_DXF ( ent logFile / )
  ; (setq ent_sel (entsel "select entity to get info"))               ; Set ent to last entity.
  ; (setq ent (car ent_sel))
  (setq entl (entget ent))           ; Set entl to association list of last entity.
  (setq ct 0)                        ; Set ct (a counter) to 0.
  (textpage)                         ; Switch to the text screen.
  (princ "\nentget of last entity:")
  (repeat (length entl)              ; Repeat for number of members in list:
    (print (nth ct entl))            ; Output a newline, then each list member.
    ; (setq out_expression (nth ct entl))
    ; (setq output_text (strcat (itoa out_expression)))
    ; (princ output_text)
    (print (nth ct entl) logFile)
    ; (if logFile
    ;   (progn
    ;     ; Write the text to the log file
        
    ;   )
    ; ); end if-then
    (setq ct (1+ ct))                ; Increments the counter by one.
  )
 (princ)                             ; Exit quietly.
)

(defun C:multi_entity_select( )
  ; select the entity for insertion point 
  (setq logFileName "/Users/franklin000/NTU/112-1/lisp/code/Final/log/demo.log") ; Change the path as needed
  (setq logFile (open logFileName "w"))
  
  ; (setq ent_sel (entsel "select entity for insertion point"))               ; Set ent to last entity.
  ; (setq main_ent (car ent_sel)) ; get the name of the entity
  ; (princ "main entity name = ")(princ main_ent)(princ "\n")
  
  (setq entlist (ssget))
  (setq total_entity (sslength entlist))
  (princ "selected number = ")(princ total_entity)(princ "\n")
  (setq i 0)
  
  (while (< i total_entity)
     
    (setq ent1 (ssname entlist i))
    (print_enetity_DXF ent1 logFile)
    (setq i (1+ i))
  )
  (princ "\ni = ")(princ i)(princ "\n")
  (princ "\nLength = ")(princ total_entity)(princ)
  (if logFile
    (progn
      ; Close the log file
      (close logFile)
      (princ (strcat "\nText exported to log file: " logFileName))
    )
    (princ "\nError: Unable to open the log file.")
    
  )
  
  
)
(defun c:Test_export ()
  (setq logFileName "/Users/franklin000/NTU/112-1/lisp/code/Final/log/demo.log") ; Change the path as needed
  ; Open the log file in append mode
  (setq logFile (open logFileName "w"))
  (ExportToLogFile FileName)
)
(defun ExportToLogFile (FileName /)
  (if logFile
    (progn
      (prompt "\nEnter text to export to the log file. Press Enter to finish.")
      (setq inputText (getstring "\nText to export: "))
      
      ; Write the text to the log file
      (princ inputText logFile)
      
      ; Close the log file
      (close logFile)
      
      (princ (strcat "\nText exported to log file: " logFileName))
    )
    (princ "\nError: Unable to open the log file.")
  )
  (princ)
)


