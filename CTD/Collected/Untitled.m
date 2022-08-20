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










