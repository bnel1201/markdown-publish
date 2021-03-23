%.html : test/%.md ./test/render_file.py
	python ./test/render_file.py $< *.html

.PHONY : clean
clean :
	del /S test\*.html