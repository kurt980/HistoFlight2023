-- Censor Trigger (Currently in use)
Delimiter //
CREATE TRIGGER censor
 BEFORE INSERT ON Comment FOR EACH ROW
  BEGIN
    SET @comment = NEW.text;
    
    IF (LOWER(@comment) LIKE "%shit%" 
		OR LOWER(@comment LIKE "%fuck%")
		OR LOWER(@comment) LIKE "%ass%"
        OR LOWER(@comment) LIKE "%bitch%"
        OR LOWER(@comment) LIKE "%damn%"
        OR LOWER(@comment) LIKE "%bastard%"
        OR LOWER(@comment) LIKE "%cunt%"
        OR LOWER(@comment) LIKE "%arse%")

	THEN
        SET NEW.text = '(The comment contains sensitive content and has been hidden)';
    END IF;         
  END//
  
  DELIMITER ;

-- Frequent user trigger (disabled)
-- DELIMITER //
-- CREATE TRIGGER freq_user
-- 	AFTER INSERT ON Comment FOR EACH ROW
-- BEGIN
-- 	
--     SET @comment_cnt = (SELECT COUNT(*) FROM Comment
-- 						WHERE user_name = NEW.user_name);
-- 	SET @us_n = NEW.user_name;
--     
-- 	IF @comment_cnt >= 3 THEN 
-- 		UPDATE Comment
-- 		SET user_name = @us_n + "(frequent commenter)"
-- 		WHERE user_name = NEW.user_name;
-- 	END IF;

-- END;




