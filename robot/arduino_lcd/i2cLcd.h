#ifndef I2CLCD_FJ27582
#define I2CLCD_FJ27582 1
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

#define SCREEN_WIDTH 16
#define SCREEN_HEIGHT 2

String clip(String inp, int start, int limit = SCREEN_WIDTH) {
    String outp = "";
    int l = inp.length();
    if(start >= l){
        return outp;
    }
    for(int a = 0;a<l;a++){
        if(a >= limit){
            break;
        }
        outp += inp[a+start];

    }
    return outp;
}

class LcdWords {
    private:
        String words[SCREEN_HEIGHT];
        String words_now_show[SCREEN_HEIGHT];
        int position_x[SCREEN_HEIGHT];
        bool scroll[SCREEN_HEIGHT];
        int rollback_rate = 300;
        unsigned long now_time[SCREEN_HEIGHT];
    public:
        LcdWords() {
            for(int a=0;a<SCREEN_HEIGHT;a++){
                now_time[a] = millis();
            }
        }
        void set_rollback_rate(int inp) {
            rollback_rate = inp;
            return;
        }
        void set_words(int pos_y, String inp, bool auto_scroll = true, bool need_scroll = false) {
            inp += " ";
            words[pos_y] = inp;
            words_now_show[pos_y] = clip(inp, 0);
            position_x[pos_y] = 0;
            if(auto_scroll){
                if(inp.length() >= SCREEN_WIDTH) {
                    scroll[pos_y] = true;
                }else{
                    scroll[pos_y] = false;
                }
            }else{
                scroll[pos_y] = need_scroll;
            }
        }
        void start_service() {
            for(int a=0;a<SCREEN_HEIGHT;a++){
                unsigned long tn = millis();
                if(scroll[a]){
                    if(tn - now_time[a] >= rollback_rate){
                        position_x[a] += 1;
                        Serial.print(position_x[a]);
                        Serial.print(" ");
                        Serial.println(words[a].length());
                        if(position_x[a] >= words[a].length()) {
                            position_x[a] = 0;
                        }
                        words_now_show[a] = clip(words[a], position_x[a]);
                        now_time[a] = tn;
                    }
                }
                
            }
        }
        void show(LiquidCrystal_I2C &l) {
            for(int a=0;a<SCREEN_HEIGHT; a++){
                l.setCursor(0, a);
                l.print(words_now_show[a].c_str());
            }
        }

};
#endif