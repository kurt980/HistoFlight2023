-- Censor Trigger (New Version, Currently in use)
Delimiter //
CREATE TRIGGER censor_insert
 BEFORE INSERT ON Comment FOR EACH ROW
  BEGIN
	-- declare bad word variable
    DECLARE badw TEXT;
    
    -- temporary table for all bad words
	CREATE TEMPORARY TABLE temp1(
		idx INT,
        words VARCHAR(50));
	INSERT INTO temp1 VALUES
							(1, "shit" ),
                            (2, "fuck"),
                            (3, "ass"),
                            (4, "bitch"),
                            (5, "dick"),
                            (6, "bastard"),
                            (7, "cunt"),
                            (8, "pussy"),
                            (9, "cock"),
							(10, "arse");
	
	-- fetch text
	SET @comment = NEW.text;
	-- get counter and maxid for while loop
	SET @counter = 1;
	SET @maxid = 10;
    
    -- loop through all bad words and censor
	WHILE (@counter < @maxid) DO
		-- fetch current bad word
        SELECT * INTO badw FROM (SELECT words FROM temp1 WHERE idx = @counter) t0;
        
        -- check if the text contains current bad word
        IF (LOWER(@comment) LIKE CONCAT("%",badw,"%"))
        THEN 
			-- replace the bad word with stars
			SET @comment = REPlACE(@comment, badw, CONCAT(SUBSTRING(badw,1,1), '***'));
        END IF;
        
        -- move to next bad word
		SET @counter = @counter + 1;
	END WHILE;
	
    SET NEW.text = CONCAT(@comment, ' (PLEASE BE POLITE!)');
    
    DROP TEMPORARY TABLE temp1;
    
END//

DELIMITER ;


-- -- Censor Trigger (Old version, Currently disabled)
-- Delimiter //
-- CREATE TRIGGER censor
--  BEFORE INSERT ON Comment FOR EACH ROW
--   BEGIN

--     -- fetch text
-- 	SET @comment = NEW.text;

--     
--     IF (LOWER(@comment) LIKE "%shit%" 
-- 		OR LOWER(@comment LIKE "%fuck%")
-- 		OR LOWER(@comment) LIKE "%ass%"
--         OR LOWER(@comment) LIKE "%bitch%"
--         OR LOWER(@comment) LIKE "%damn%"
--         OR LOWER(@comment) LIKE "%bastard%"
--         OR LOWER(@comment) LIKE "%cunt%"
--         OR LOWER(@comment) LIKE "%arse%")

-- 	THEN
--         SET NEW.text = '(The comment contains sensitive content and has been hidden)';
--     END IF;         
--   END//
--   
--   DELIMITER ;



-- -- Frequent user trigger (disabled)
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




