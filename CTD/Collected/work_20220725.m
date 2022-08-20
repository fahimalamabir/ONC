% sample working script

close all; clearvars

%load dataset
load('dataset_anl_137E.mat')

%load climate index dataset
Cli =importdata('Index.xls');
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Calculate long-time (i.e., climatological) mean
P        =nanmean(data.P,3);

T_mean   =nanmean(data.T,3);
S_mean   =nanmean(data.S,3);
PT_mean  =nanmean(data.PT,3);
Sig_mean =nanmean(data.Sig,3);

%Plot sectional distribution of climatological salinity
figure('Position',[0,0,1200,800])
[C,h] =contourf(data.lat,[0:2030],S_mean,[32.0:0.1:35.0]);
xlabel('Latitude [deg N]')
ylabel('Pressure [dbar]')
cl=colorbar; 
caxis([33.8,35.2]); 
axis ij;
set(gca,'ylim',[0,1000],'xdir','reverse','Fontsize',20)
ylabel(cl,'Mean Salinity')
colormap(jet); 
set(h,'ShowText','on','LineWidth',1)
clabel(C,h,'Fontsize',16,'LabelSpacing',800);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Calculate long-time (i.e., climatological) mean for each season (i.e, summer and winter)
%winter
q               =data.mon==1;
P(:,:,2)        =nanmean(data.P(:,:,q),3);
T_mean(:,:,2)   =nanmean(data.T(:,:,q),3);
S_mean(:,:,2)   =nanmean(data.S(:,:,q),3);
PT_mean(:,:,2)  =nanmean(data.PT(:,:,q),3);
Sig_mean(:,:,2) =nanmean(data.Sig(:,:,q),3);

%summer
q               =data.mon~=1;
P(:,:,3)        =nanmean(data.P(:,:,q),3);
T_mean(:,:,3)   =nanmean(data.T(:,:,q),3);
S_mean(:,:,3)   =nanmean(data.S(:,:,q),3);
PT_mean(:,:,3)  =nanmean(data.PT(:,:,q),3);
Sig_mean(:,:,3) =nanmean(data.Sig(:,:,q),3);


%Plot sectional distribution of climatological potential temperature for
%winter
figure('Position',[0,0,1200,800])
[C,h] =contourf(data.lat,[0:2030],PT_mean(:,:,2),[0:2:30]);
xlabel('Latitude [deg N]')
ylabel('Pressure [dbar]')
cl=colorbar; 
caxis([0,30]); 
axis ij;
set(gca,'ylim',[0,1000],'xdir','reverse','Fontsize',20)
ylabel(cl,'Mean potential temperature @ winter [^oC]')
colormap(redblue); 
set(h,'ShowText','on','LineWidth',1)
clabel(C,h,'Fontsize',16,'LabelSpacing',800);

% % % % %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Calculate linear tend and correlation with climate index
data_date =datenum(data.yr,data.mon,15); %middle of each month (unit in day)
S_trend   =nan(size(data.S,1),size(data.S,2)); %initialize matrix
PT_trend  =nan(size(data.PT,1),size(data.PT,2)); %initialize matrix

for ii=1:1001 %down to 1000 dbar
for jj=1:size(data.S,2) 

    %Linear trend Analysis
    q =data.yr>=1967 & data.yr<=2016 ; %1967-2016(Oka et al. 2017)

    p =polyfit(data_date(q),squeeze(data.S(ii,jj,q))',1); 
    S_trend(ii,jj) =p(1) *365; %linear trend per year

    p =polyfit(data_date(q),squeeze(data.PT(ii,jj,q))',1);
    PT_trend(ii,jj) =p(1) *365; %linear trend per year
    
    %Correlation Analysis between various climate indices 
    q        =data.mon==1 ; %winter
    yr       =data.yr(q);
    q_Cli    =Cli.data(:,1)>=min(yr) & Cli.data(:,1)<=max(yr);
    PDO      =Cli.data(q_Cli,3);    
    NPGO     =Cli.data(q_Cli,4);    
    NPGO_2yr =Cli.data(q_Cli,5);    

    %For salinity
    S_tmp   =squeeze(data.S(ii,jj,q));
    [R,p]  =corrcoef([S_tmp,PDO,NPGO,NPGO_2yr]);
    corr.S_PDO(ii,jj)       =R(1,2);
    corr.S_NPGO(ii,jj)      =R(1,3);
    corr.S_NPGO_2yr(ii,jj)  =R(1,4);
    p_val.S_PDO(ii,jj)      =p(1,2);
    p_val.S_NPGO(ii,jj)     =p(1,3);
    p_val.S_NPGO_2yr(ii,jj) =p(1,4);
    
    %For potential temperature
    PT_tmp =squeeze(data.PT(ii,jj,q));
    [R,p]  =corrcoef([PT_tmp,PDO,NPGO,NPGO_2yr]);
    corr.PT_PDO(ii,jj)       =R(1,2);
    corr.PT_NPGO(ii,jj)      =R(1,3);
    corr.PT_NPGO_2yr(ii,jj)  =R(1,4);
    p_val.PT_PDO(ii,jj)      =p(1,2);
    p_val.PT_NPGO(ii,jj)     =p(1,3);
    p_val.PT_NPGO_2yr(ii,jj) =p(1,4);
    
end
end

%plot sectional distribution of salinity trend
figure('Position',[0,0,1200,800])
contourf(data.lat,[0:2030],S_trend,20,'edgecolor','none');
xlabel('Latitude [deg N]')
ylabel('Pressure [dbar]')
set(gca,'ylim',[0,1000],'xdir','reverse','Fontsize',20)
colormap(redblue); 
cl=colorbar;
ylabel(cl,'S Trend @1967-2016 (/yr) ')
caxis([-0.005,0.005]); 
axis ij; 
hold on

%Mean Salinity contour
[C,h] =contour(data.lat,[0:2030],S_mean(:,:,1),'k-');
set(h,'LevelStep',0.1,'ShowText','on','LineWidth',1,...
    'TextStep',get(h,'LevelStep')*2)
clabel(C,h,'Fontsize',16,'LabelSpacing',800);

%plot sectional distribution of correlation between salinity and PDO
figure('Position',[0,0,1200,800])
contourf(data.lat,[0:1000],corr.S_PDO,20,'edgecolor','none');
xlabel('Latitude [deg N]')
ylabel('Pressure [dbar]')
set(gca,'ylim',[0,1000],'xdir','reverse','Fontsize',20)
colormap(redblue); 
cl=colorbar; 
ylabel(cl,'Corr Coeff between S and PDO')
caxis([-0.5,0.5]); 
axis ij; 
hold on

%Plot dots where significant correlation found
q    =p_val.S_PDO<0.05; 
Pres =data.P(1:size(p_val.S_PDO,1),:,1);
Lat  =repmat(data.lat,size(Pres,1),1);
Pres(~q) =nan;
Lat(~q)  =nan;
plot(Lat,Pres,'k*','Markersize',2)

%Mean Salinity contour
[C,h] =contour(data.lat,[0:2030],S_mean(:,:,1),'k-');
set(h,'LevelStep',0.1,'ShowText','on','LineWidth',1,...
    'TextStep',get(h,'LevelStep')*2)
clabel(C,h,'Fontsize',16,'LabelSpacing',800);


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%extract STMW, NPTW, and NPIW (Oka et al. 2018)

Area =repmat(gradient(-data.lat)*1852*60,size(data.P,1),1); %area of each data point (1 nautical mile = 1852m)
mm   =0;

for kk=1:size(data.P,3)
    if(data.mon(kk)~=1) %Summer
        mm=mm+1;
        
        q_STMW =data.PV(:,:,kk) <2.0 *10^-10 & data.PT(:,:,kk)>=16 & data.PT(:,:,kk)<=19.5; %Suga et al. 1989
        q_NPTW =data.S(:,:,kk)  >34.9        & repmat(data.lat,size(data.P,1),1)>7; %Suga et al. 2000
        q_NPIW =data.S(:,:,kk)  <34.2        & data.P(:,:,kk) >200; %Shuto 1996

        STMW.Area(mm) = sum(Area(q_STMW));
        STMW.PT(mm)   = nanmean(data.PT(q_STMW));
        STMW.S(mm)    = nanmean(data.S(q_STMW));
        STMW.yr(mm)   = data.yr(kk);

        NPTW.Area(mm) = sum(Area(q_NPTW));
        NPTW.PT(mm)   = nanmean(data.PT(q_NPTW));
        NPTW.S(mm)    = nanmean(data.S(q_NPTW));
        NPTW.yr(mm)   = data.yr(kk);

        NPIW.Area(mm) = sum(Area(q_NPIW));
        NPIW.PT(mm)   = nanmean(data.PT(q_NPIW));
        NPIW.S(mm)    = nanmean(data.S(q_NPIW));
        NPIW.yr(mm)   = data.yr(kk);        
        
    end
end

%plot timeseries of STMW Area
figure('Position',[0,0,1200,800])
plot(STMW.yr, STMW.Area,'k-','linewidth',5)
set(gca,'xlim',[1970,2023],'fontsize',20)
ylabel('STMW Area @summer (m^2)')
xlabel('Year')
hold on













