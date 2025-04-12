#include <hpgcc49.h>
#include <hpgraphics.h>
#include <hpstdio.h>
#include <hpkeyb49.h>
#include <hpstring.h>

#include <stdint.h>
extern uint8_t *__display_buf;
extern U32 syscallArg0(U32 index);
extern void _hpg_set_mode(int mode,char *visfb, char *drawfb,
    void (*drawfn)(hpg_t *, int, int, int, int, int),
    unsigned char (*getfn)(hpg_t *, int, int));
extern void _hpg_gray16_draw(hpg_t *g, int x, int y, int len, int patx, int paty);
extern unsigned char _hpg_gray16_get(hpg_t *g, int x, int y);


int main() 
{
	char name[40]="";
	gets(name);
	
	hpg_init();
	char *plane1;
	char *plane2;
	uint32_t *plane_k;
	uint32_t *plane_t;
	//char *t;
	plane2 = plane1 = (char *) sys_phys_malloc(6820);
	_hpg_set_mode(MODE_16GRAY,plane1, plane2,_hpg_gray16_draw, _hpg_gray16_get);
	plane_k=(uint32_t *)plane1;
	/*if(name==NULL)
	{
		strcpy(name,"badapp.bin");
	}*/
	syscallArg0(19);
	sys_setupTimers();
	//hpg_set_mode_mono(0);
	//hpg_set_mode_gray16(0);
	/*FS_FILE *video;
	FSOpen("1.bin",FSMODE_READ,&video);*/
	FILE *video;
	video=fopen(name,"r");
	
	if(video==NULL)
	{
		puts(name);
		puts(" Failed!");
		sys_restoreTimers();
		//FSClose(video);
		fclose(video);
		return 0;
	}
	
	int k,h;
	int readnum=1;
	//int timer=0;
	double speed=1.0;
	int wait=7000;
	volatile unsigned char j,i;
	uint32_t* buf;
	//buf=(char*)malloc(1040);
	hpg_clear();
	buf=(uint32_t*)malloc(1040*4);
	while(fread(buf,4160,1,video)==1){
		//readnum=fread(buf,4160,1,video);
		h=13;
		for(i=1;i<79;i++)
		{	
			
			/*for(j=2;j<15;j++)
			{
				*(plane_k+i*20+j)=buf[h++];
			}*/
			plane_t=plane_k+i*20;
			*(plane_t+2)=buf[h++];
			*(plane_t+3)=buf[h++];
			*(plane_t+4)=buf[h++];
			*(plane_t+5)=buf[h++];
			
			*(plane_t+6)=buf[h++];
			*(plane_t+7)=buf[h++];
			*(plane_t+8)=buf[h++];
			*(plane_t+9)=buf[h++];
			
			*(plane_t+10)=buf[h++];
			*(plane_t+11)=buf[h++];
			*(plane_t+12)=buf[h++];
			*(plane_t+13)=buf[h++];
			
			*(plane_k+i*20+14)=buf[h++];
		}
		if(keyb_isAnyKeyPressed()==1)
		{
				if(keyb_isLeft()==1)
				{
					if(7000.0*speed>1&&speed!=speed*1.25){speed=speed*1.25;wait=7000.0*speed;}
				}
				else if(keyb_isRight()==1)
				{
					speed=1.0*speed/1.25;
					wait=7000.0*speed;
				}
				else if(keyb_isUp()==1)
				{
					speed=1.0;
				}
				else
				{
					break;
				}
				//timer=k;
				putchar('\f');
				printf("%d %f",wait,speed);
				sys_waitTicks(14000);
			
		}
		sys_waitTicks(wait);
	}
	//printf("%d %f",wait,speed);
	//gets(name);
	sys_restoreTimers();
	free(buf);
	fclose(video);
	return 0;
}
